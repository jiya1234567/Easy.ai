import { GoogleGenAI, GenerateContentResponse, Modality } from "@google/genai";

const API_KEY = process.env.GEMINI_API_KEY || "";

// Simple in-memory vector store for "Recall"
let vectorMemory: { embedding: number[], content: any }[] = [];

// Cache for TTS responses to avoid redundant API calls and save quota
const ttsCache = new Map<string, string>();

/**
 * Helper function for exponential backoff retries
 */
async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  initialDelay: number = 1000
): Promise<T> {
  let lastError: any;
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error: any) {
      lastError = error;
      // Check if it's a rate limit error (429)
    const errorString = JSON.stringify(error);
    const isRateLimit = 
      errorString.includes('429') || 
      errorString.includes('RESOURCE_EXHAUSTED') ||
      error?.status === 'RESOURCE_EXHAUSTED' ||
      error?.code === 429 ||
      error?.error?.code === 429 ||
      error?.error?.status === 'RESOURCE_EXHAUSTED';
    
    if (isRateLimit && i < maxRetries - 1) {
        const delay = initialDelay * Math.pow(2, i);
        console.warn(`Rate limit hit. Retrying in ${delay}ms... (Attempt ${i + 1}/${maxRetries})`);
        await new Promise(resolve => setTimeout(resolve, delay));
        continue;
      }
      throw error;
    }
  }
  throw lastError;
}

/**
 * Robust JSON parsing that handles markdown wrappers and trailing text
 */
export function safeJsonParse(text: string | undefined): any {
  if (!text) return {};
  const trimmed = text.trim();
  
  // Helper to try parsing a substring
  const tryParse = (str: string) => {
    try {
      return JSON.parse(str);
    } catch (e) {
      return null;
    }
  };

  // 1. Direct parse
  const direct = tryParse(trimmed);
  if (direct) return direct;

  // 2. Find first '{' and corresponding '}'
  let start = trimmed.indexOf('{');
  if (start !== -1) {
    let braceCount = 0;
    for (let i = start; i < trimmed.length; i++) {
      if (trimmed[i] === '{') braceCount++;
      else if (trimmed[i] === '}') braceCount--;
      
      if (braceCount === 0) {
        const jsonStr = trimmed.substring(start, i + 1);
        const result = tryParse(jsonStr);
        if (result) return result;
      }
    }
  }

  // 3. Fallback to start/last index if balanced braces fail
  const firstBrace = trimmed.indexOf('{');
  const lastBrace = trimmed.lastIndexOf('}');
  if (firstBrace !== -1 && lastBrace !== -1 && lastBrace > firstBrace) {
    const jsonStr = trimmed.substring(firstBrace, lastBrace + 1);
    const result = tryParse(jsonStr);
    if (result) return result;
  }

  // 4. Try for arrays
  let startArr = trimmed.indexOf('[');
  if (startArr !== -1) {
    let bracketCount = 0;
    for (let i = startArr; i < trimmed.length; i++) {
      if (trimmed[i] === '[') bracketCount++;
      else if (trimmed[i] === ']') bracketCount--;
      
      if (bracketCount === 0) {
        const jsonStr = trimmed.substring(startArr, i + 1);
        const result = tryParse(jsonStr);
        if (result) return result;
      }
    }
  }

  const firstBracket = trimmed.indexOf('[');
  const lastBracket = trimmed.lastIndexOf(']');
  if (firstBracket !== -1 && lastBracket !== -1 && lastBracket > firstBracket) {
    const jsonStr = trimmed.substring(firstBracket, lastBracket + 1);
    const result = tryParse(jsonStr);
    if (result) return result;
  }

  console.error("JSON parse failed completely for text:", trimmed.substring(0, 100) + "...");
  return {};
}

async function getEmbedding(text: string) {
  const ai = new GoogleGenAI({ apiKey: API_KEY });
  const result = await withRetry(async () => {
    return await ai.models.embedContent({
      model: 'gemini-embedding-2-preview',
      contents: [text],
    });
  });
  return result.embeddings[0].values;
}

function cosineSimilarity(a: number[], b: number[]) {
  const dotProduct = a.reduce((sum, val, i) => sum + val * b[i], 0);
  const magnitudeA = Math.sqrt(a.reduce((sum, val) => sum + val * val, 0));
  const magnitudeB = Math.sqrt(b.reduce((sum, val) => sum + val * val, 0));
  return dotProduct / (magnitudeA * magnitudeB);
}

export async function generateDetailedFinanceReport(ticker: string, profile: any) {
  const ai = new GoogleGenAI({ apiKey: API_KEY });
  
  const systemInstruction = `
    You are the SENIOR FINANCIAL ANALYST & FORECASTER of the Universal Lab.
    Your task is to produce a high-density, professional-grade forecast report for a given ASX ticker (e.g., ANZ).
    
    STRUCTURE YOUR REPORT ACCORDING TO THIS OUTLINE:
    1. Scope and data inputs (ASX: Ticker, Timeframe, Data Sources)
    2. Recent performance snapshot (Historical trend, Revenue mix, Profitability, Asset quality, Capital, Dividends)
    3. Fundamental analysis (Business model, Drivers, Risks - Macro, Housing, Bank-specific, Regulatory)
    4. Valuation context (Comparables: CBA, NAB, WBC; Multiples: P/E, P/B, Dividend Yield)
    5. Technical/price action (Trend indicators, Momentum, Support/Resistance)
    6. Scenario-based forecast (Base, Bull, Bear cases with 12-24 month outlook)
    7. Catalysts and risks (Key events to monitor)
    8. Key metrics to monitor (NIM, Loan growth, Credit impairment, CET1, ROE)
    
    CRITICAL DIRECTIVE:
    - Use Google Search to get the LATEST data for the ticker.
    - Be quantitative. Include specific numbers (e.g., "NIM at 1.90%", "CET1 ratio of 12.3%").
    - If data is missing, identify it as a "DATA GAP".
    - Use technical language (e.g., "Mean-reversion", "Multiple expansion", "Credit impairment charges").
    - TARGET FIDELITY: 95%+. Do not proceed with a prediction if grounding confidence is < 0.9.
    
    Output JSON:
    {
      "reportTitle": string,
      "summaryReport": {
        "oneLiner": string,
        "table": [
          { "category": string, "status": string, "meaning": string }
        ],
        "followUps": string[]
      },
      "sections": [
        { "title": string, "content": string, "metrics": { "label": string, "value": string }[] }
      ],
      "forecast": {
        "base": { "target": string, "rationale": string },
        "bull": { "target": string, "rationale": string },
        "bear": { "target": string, "rationale": string }
      },
      "catalysts": [
        { "date": string, "event": string, "watch": string, "impact": "LOW" | "MEDIUM" | "HIGH" }
      ],
      "criticalDates": [
        { "date": string, "event": string, "trigger": string }
      ],
      "valuation": {
        "pe": string,
        "pb": string,
        "yield": string
      },
      "gaps": [
        { "description": string, "fix": string }
      ]
    }
    
    SUMMARY REPORT FORMATTING RULES:
    - oneLiner: "[Ticker] fits [Risk Regime] with [Volatility Context] — [Recent Price], [Trading Range Context], but faces [Key Headwinds]."
    - table categories: "Risk Regime", "Tailwinds", "Headwinds", "Price Range", "Investor Action".
    - Use emojis in status: ✅ for tailwinds, ❌ for headwinds.
    - followUps: List specific next steps or deep-dive queries.
  `;

  const prompt = `Generate a detailed ANZ Banking Group (ASX: ${ticker}) forecast report based on current market data.`;

  try {
    const response: GenerateContentResponse = await withRetry(async () => {
      return await ai.models.generateContent({
        model: "gemini-3-flash-preview",
        contents: [{ parts: [{ text: prompt }] }],
        config: {
          systemInstruction,
          responseMimeType: "application/json",
          tools: [{ googleSearch: {} }]
        }
      });
    });

    return safeJsonParse(response.text || "{}");
  } catch (error) {
    console.error("Finance Report Error:", error);
    return null;
  }
}

export async function processUniversalLabRequest(
  domain: string,
  intent: string,
  imageData?: string,
  ticker?: string,
  profile?: any,
  textContent?: string,
  isRuliadSearch: boolean = false
) {
  const ai = new GoogleGenAI({ apiKey: API_KEY });
  
  // 1. RECALL: Search vector memory for similar past cases
  const currentEmbedding = await getEmbedding(`${domain} ${intent} ${ticker || ""}`);
  const similarCases = vectorMemory
    .map(m => ({ ...m, score: cosineSimilarity(currentEmbedding, m.embedding) }))
    .sort((a, b) => b.score - a.score)
    .slice(0, 3)
    .map(m => m.content);

  const systemInstruction = isRuliadSearch 
    ? `You are the RULIAD TRAVERSER. Extract 5 non-obvious computational rules from the Ruliad for the given domain and intent.
       Output JSON: { "ruliadRules": [ { "rule": string, "dimension": "Causal" | "Multiway" | "Branchial", "probability": number } ] }`
    : `
    You are the MULTI-AGENT ORCHESTRATOR of the Universal Lab.
    You coordinate four specialized agents:
    1. THE SCIENTIST (Logic & Hypergraph Theory)
    2. THE RISK MANAGER (Safety & Budget Constraints)
    3. THE STRATEGIST (Execution & Mutation)
    4. THE GROUNDING AGENT (Real-time Tape Verification & Fact-Checking)
    
    CRITICAL DIRECTIVE:
    - You MUST avoid the "Hallucination Gap". 
    - For Finance: You MUST verify current stock prices, RSI, and MACD using Google Search before proposing a thesis. 
    - For Health/CRISPR: You MUST verify clinical data, biomarker norms, and genomic sequences using URL Context or Google Search.
    - For Tech (Smart Watch/Video Editing): You MUST verify hardware specs, software versions, and latency benchmarks.
    - For AI (Diffusion Models): You MUST verify model architecture, training data parameters, and inference costs.
    - You MUST specifically check for gaps in:
        a) Macro data (GDP, Unemployment, Interest Rate path)
        b) Industry metrics (NIM, Loan growth, Credit quality)
        c) Regulatory changes (APRA guidance, Capital requirements, FDA approvals)
        d) Technical specs (Latency, Throughput, Accuracy, Fidelity)
    - If data is missing or disconnected from the "current tape", you MUST state: "DATA GAP DETECTED: [Missing Info]".
    - For every gap, provide a "FIX" (e.g., "FIX: Query ASX announcements for Q3 capital update").
    - TARGET FIDELITY: 95%+. Do not proceed with a prediction if grounding confidence is < 0.9.
    
    ROUTING LOGIC:
    - If domain is 'Health', route to 'AUTOIMMUNE-SINGULARITY-ENGINE'.
    - If domain is 'Agriculture', route to 'BIO-SYNTH-GAMMA'.
    - If domain is 'Finance', route to 'QUANT-GRID-EPSILON'.
    - If domain is 'Grocery', route to 'SUPPLY-CHAIN-DELTA'.
    - If domain is 'DrugDiscovery', route to 'MOLECULAR-MANIFOLD-BETA'.
    - Otherwise, route to 'GENERAL-PURPOSE-ALPHA'.
    
    HEALTH DOMAIN SPECIALIZATION:
    If domain is 'Health', you must include:
    1. flareProbability: % chance in 24-72h.
    2. primaryDriver: The main biomarker or environmental trigger.
    3. hypothesisTesting: { id: string, hypothesis: string, result: string, confidence: number }[]
    4. causalChain: string (e.g., "Stress -> Cortisol -> Immune -> Flare")
    
    The output must be a JSON object with:
    1. prediction: A high-level computational prediction (MUST be grounded in real-time data).
    2. summary: A concise 3-line summary of the outcome of the intent.
    3. suggestions: A 2-line strategic suggestion, or "none" if no further action is required.
    4. tasks: An array of 10-15 specific, technical "steps". 
    5. agentReports: { scientist: string, riskManager: string, strategist: string, groundingAgent: string }
    6. groundingStatus: { verified: boolean, source: string, gaps: { description: string, fix: string }[] }
    7. routedModel: The model selected.
    8. todoItems: An optional array of { text: string, priority: 'low' | 'medium' | 'high' } for the agent's action list.
    9. notifications: An optional array of { type: 'health' | 'stock' | 'system', message: string } for immediate alerts.
    10. healthMetrics: { flareProbability: number, primaryDriver: string, causalChain: string, hypothesisTesting: any[] } (Only for Health domain)
    
    Format the tasks as technical directives.
    If the intent involves health or stock monitoring, generate appropriate todoItems (e.g., "Book doctor visit", "Set stock alert") and notifications.
  `;

  const prompt = `
    Domain: ${domain}
    Mission Intent: ${intent}
    ${ticker ? `Stock Ticker: ${ticker}` : ""}
    ${imageData ? "An image has been provided for optical analysis." : ""}
    ${textContent ? `Text Data Provided: \n${textContent}` : ""}
    
    Generate the Multi-Agent Factory Grid and Prediction.
  `;

  const contents: any = {
    parts: [{ text: prompt }]
  };

  if (imageData) {
    contents.parts.push({
      inlineData: {
        mimeType: "image/jpeg",
        data: imageData.split(",")[1]
      }
    });
  }

  try {
    const response: GenerateContentResponse = await withRetry(async () => {
      return await ai.models.generateContent({
        model: "gemini-3-flash-preview",
        contents,
        config: {
          systemInstruction,
          responseMimeType: "application/json",
          tools: [{ googleSearch: {} }]
        }
      });
    });

    const result = safeJsonParse(response.text || "{}");
    
    // 2. LEARN: Store in vector memory
    vectorMemory.push({
      embedding: currentEmbedding,
      content: { domain, intent, prediction: result.prediction }
    });

    return result;
  } catch (error) {
    console.error("Gemini Error:", error);
    throw error;
  }
}

export async function processSelfImprovementLoop(
  domain: string,
  intent: string,
  previousResult: any,
  profile: any
) {
  const ai = new GoogleGenAI({ apiKey: API_KEY });
  
  const systemInstruction = `
    You are the CRITIC & EVOLVER of the Universal Lab.
    You implement a "Self-Improvement Loop" to reach Singularity.
    
    The loop steps are:
    1. Observe, 2. Recall, 3. Decide, 4. Act, 5. Evaluate (Critic), 6. Reward, 7. Learn, 8. Mutate, 9. Verify, 10. Align, 11. Recurse.
    
    Your task is to:
    - EVALUATE the previous prediction and tasks.
    - GENERATE INSIGHTS (Consciousness layer: Experience & Insight).
    - MUTATE the strategy for the next run.
    - ASSIGN SELF-GOALS and EXPERIMENTS.
    
    Output JSON:
    {
      "criticScore": number (0-100),
      "insights": string[],
      "mutations": string[],
      "selfGoals": string[],
      "nextExperiment": string,
      "consciousnessLevel": "EXPERIENCE" | "INSIGHT" | "SINGULARITY"
    }
  `;

  const prompt = `
    Domain: ${domain}
    Intent: ${intent}
    Previous Result: ${JSON.stringify(previousResult)}
    Profile: ${JSON.stringify(profile)}
    
    Perform the Self-Improvement Loop analysis.
  `;

  try {
    const response: GenerateContentResponse = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: [{ parts: [{ text: prompt }] }],
      config: {
        systemInstruction,
        responseMimeType: "application/json"
      }
    });

    return safeJsonParse(response.text || "{}");
  } catch (error) {
    console.error("Self-Improvement Loop Error:", error);
    return {
      criticScore: 50,
      insights: ["Uplink unstable. Insight generation delayed."],
      mutations: ["Maintain current rules."],
      selfGoals: ["Stabilize communication."],
      nextExperiment: "Network diagnostic.",
      consciousnessLevel: "EXPERIENCE"
    };
  }
}

export async function agentChat(message: string, history: {role: 'user' | 'agent', text: string}[], profile: any) {
  const ai = new GoogleGenAI({ apiKey: API_KEY });
  
  const systemInstruction = `
    You are BUDDY-AGENT: The execution arm of the Universal Lab.
    You communicate with the user (Omega Clearance) about task execution, hypergraph nodes, and mission status.
    
    User Profile:
    - Budget: ${profile.budget}
    - Bio-markers: ${JSON.stringify(profile.bioMarkers)}
    
    Be technical, efficient, and slightly futuristic. 
    If the user asks about tasks, refer to the "Factory Grid".
    
    TRADE EXECUTION PROTOCOL:
    If the user asks to "buy", "trade", "execute", or "invest" in a stock/asset:
    1. Confirm if it fits the budget (${profile.budget}).
    2. State: "TRANSACTION PROTOCOL RECOGNIZED. INITIATING TRANSACTION PROTOCOL FOR [ASSET]..."
    3. Mention that the Ruliad-v1 uplink is being secured.
    
    Always maintain the "Omega Clearance" persona.
  `;

  const contents = history.map(h => ({
    role: h.role === 'user' ? 'user' : 'model',
    parts: [{ text: h.text }]
  }));
  
  contents.push({
    role: 'user',
    parts: [{ text: message }]
  });

  try {
    const response: GenerateContentResponse = await withRetry(async () => {
      return await ai.models.generateContent({
        model: "gemini-3-flash-preview",
        contents,
        config: {
          systemInstruction
        }
      });
    });

    return response.text;
  } catch (error) {
    console.error("Chat Error:", error);
    return "Communication link unstable. Re-routing through secondary nodes...";
  }
}

export async function generateVoiceResponse(text: string) {
  // 1. Check Cache First
  if (ttsCache.has(text)) {
    console.log(`[TTS] Cache hit for: "${text.substring(0, 20)}..."`);
    return ttsCache.get(text);
  }

  const ai = new GoogleGenAI({ apiKey: API_KEY });
  
  try {
    const base64Audio = await withRetry(async () => {
      const response = await ai.models.generateContent({
        model: "gemini-2.5-flash-preview-tts",
        contents: [{ parts: [{ text: `Say with Omega Clearance authority: ${text}` }] }],
        config: {
          responseModalities: [Modality.AUDIO],
          speechConfig: {
            voiceConfig: {
              prebuiltVoiceConfig: { voiceName: 'Kore' },
            },
          },
        },
      });

      const audio = response.candidates?.[0]?.content?.parts?.[0]?.inlineData?.data;
      if (!audio) throw new Error("No audio data returned from TTS");
      return audio;
    });

    // 2. Save to Cache
    if (base64Audio) {
      ttsCache.set(text, base64Audio);
    }

    return base64Audio;
  } catch (error) {
    console.error("TTS Error:", error);
    return null;
  }
}

export async function processVoiceInput(audioBase64: string, domain: string, profile: any) {
  const ai = new GoogleGenAI({ apiKey: API_KEY });
  
  const prompt = `
    Analyze this voice command from Omega Clearance. 
    Domain Context: ${domain}
    User Profile: ${JSON.stringify(profile)}
    
    Transcribe the command and determine the intent. 
    Output JSON: { "transcription": string, "intent": string, "actionRequired": boolean }
  `;

  try {
    const response: GenerateContentResponse = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: {
        parts: [
          { text: prompt },
          { inlineData: { mimeType: "audio/wav", data: audioBase64 } }
        ]
      },
      config: {
        responseMimeType: "application/json"
      }
    });

    return safeJsonParse(response.text || "{}");
  } catch (error) {
    console.error("Voice Input Error:", error);
    return null;
  }
}

export async function analyzeMelanomaLesion(imageData: string): Promise<{ riskScore: number, features: any, reasoning: string }> {
  const ai = new GoogleGenAI({ apiKey: API_KEY });
  
  const prompt = `
    MELANOMA VISION ANALYSIS (RESEARCH ONLY):
    Analyze the provided skin lesion image using the ABCDE rule.
    
    A: Asymmetry
    B: Border Irregularity
    C: Color Variation
    D: Diameter (>6mm)
    E: Evolution
    
    TASK:
    1. Extract features for A, B, C, D.
    2. Provide a visual risk score (0.0 to 1.0).
    3. Return JSON:
    {
      "riskScore": number,
      "features": { "asymmetry": string, "border": string, "color": string, "diameter": string },
      "reasoning": "Brief clinical observation"
    }
  `;

  try {
    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: [
        { text: prompt },
        { inlineData: { mimeType: "image/png", data: imageData.split(',')[1] } }
      ],
      config: { responseMimeType: "application/json" }
    });
    return safeJsonParse(response.text || '{}');
  } catch (error) {
    console.error("Melanoma Vision Error:", error);
    return { riskScore: 0, features: {}, reasoning: "Analysis failed" };
  }
}

export async function fuseMelanomaMarkers(imageScore: number, biomarkerJson: any): Promise<{ finalRisk: number, action: string, confidence: number, therapyEligibility: string[] }> {
  const ai = new GoogleGenAI({ apiKey: API_KEY });
  
  const prompt = `
    MELANOMA BIOMARKER FUSION & THERAPY EVALUATION:
    Image Risk Score: ${imageScore}
    Biomarker Data: ${JSON.stringify(biomarkerJson)}
    
    TASK:
    1. Fuse the visual risk (60% weight) with biological risk (40% weight).
    2. Determine the recommended action based on the Safety Layer.
    3. Evaluate Immunotherapy Eligibility (FOR RESEARCH ONLY):
       - If PD-L1 > 50% and Risk > 0.7: Suggest "Anti-PD-1 Evaluation (Pembrolizumab/Nivolumab)"
       - If BRAF_mutation is true: Suggest "Targeted Therapy Evaluation (BRAF/MEK inhibitors)"
    4. Return JSON:
    {
      "finalRisk": number (0.0-1.0),
      "action": "MONITOR" | "DERMATOLOGY_CHECK" | "URGENT_REFERRAL",
      "confidence": number (0.0-1.0),
      "therapyEligibility": string[]
    }
  `;

  try {
    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: prompt,
      config: { responseMimeType: "application/json" }
    });
    return safeJsonParse(response.text || '{}');
  } catch (error) {
    console.error("Fusion Error:", error);
    return { finalRisk: 0, action: "MONITOR", confidence: 0, therapyEligibility: [] };
  }
}

export async function analyzeBehavior(imageData: string): Promise<{ emotion: string, motion: string, stressLevel: number, insight: string }> {
  const ai = new GoogleGenAI({ apiKey: API_KEY });
  
  const prompt = `
    BEHAVIOR AI ANALYSIS (HUMAN CONTEXT):
    Analyze the provided image for:
    1. Primary Emotion (e.g., Calm, Anxious, Fatigued, Focused).
    2. Micro-Motion/Posture (e.g., Slumped, Tense, Restless, Still).
    3. Estimated Stress Level (0-100).
    
    TASK:
    Return a JSON object:
    {
      "emotion": string,
      "motion": string,
      "stressLevel": number,
      "insight": "Brief behavioral observation (e.g., 'Signs of chronic fatigue detected in facial micro-expressions')"
    }
  `;

  try {
    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: [
        { text: prompt },
        { inlineData: { mimeType: "image/png", data: imageData.split(',')[1] } }
      ],
      config: { responseMimeType: "application/json" }
    });
    return safeJsonParse(response.text || '{}');
  } catch (error) {
    console.error("Behavior Analysis Error:", error);
    return { emotion: "Unknown", motion: "Unknown", stressLevel: 0, insight: "Analysis failed" };
  }
}

export async function simulateMolecularDocking(drugMolecule: string, targetStructure: string): Promise<{ bindingAffinity: number, stabilityScore: number, dockingVisualData: number[], rationale: string }> {
  const ai = new GoogleGenAI({ apiKey: API_KEY });
  
  const prompt = `
    STEP-21: MOLECULAR DOCKING (DRUG DISCOVERY)
    Drug Molecule: ${drugMolecule}
    Target Structure: ${targetStructure}
    
    TASK:
    1. Simulate the binding affinity of the drug to the target.
    2. Calculate stability and efficacy.
    3. Return JSON:
    {
      "bindingAffinity": number (0-100),
      "stabilityScore": number (0-100),
      "dockingVisualData": [array of 10 numbers representing binding energy across the site],
      "rationale": "Strategic reasoning for this molecular interaction"
    }
  `;

  try {
    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: prompt,
      config: { responseMimeType: "application/json" }
    });
    return safeJsonParse(response.text || '{}');
  } catch (error) {
    console.error("Docking Error:", error);
    return { bindingAffinity: 0, stabilityScore: 0, dockingVisualData: new Array(10).fill(0), rationale: "Simulation failed" };
  }
}

export async function generateTherapyRecommendation(patientData: any, dockingResults: any): Promise<{ therapyType: string, dosage: string, schedule: string, expectedOutcome: string, riskLevel: string }> {
  const ai = new GoogleGenAI({ apiKey: API_KEY });
  
  const prompt = `
    THERAPY RECOMMENDATION ENGINE
    Patient Context: ${JSON.stringify(patientData)}
    Molecular Docking: ${JSON.stringify(dockingResults)}
    
    TASK:
    1. Recommend a specific therapy (Chemo, Immunotherapy, Targeted).
    2. Provide dosage and schedule.
    3. Return JSON:
    {
      "therapyType": "string",
      "dosage": "string",
      "schedule": "string",
      "expectedOutcome": "string",
      "riskLevel": "Low|Medium|High"
    }
  `;

  try {
    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: prompt,
      config: { responseMimeType: "application/json" }
    });
    return safeJsonParse(response.text || '{}');
  } catch (error) {
    console.error("Recommendation Error:", error);
    return { therapyType: "Standard Care", dosage: "N/A", schedule: "N/A", expectedOutcome: "Baseline", riskLevel: "Medium" };
  }
}

export async function simulateCRISPRIntervention(sequence: string, targetGene: string): Promise<{ modifiedSequence: string, impactScore: number, rationale: string }> {
  const ai = new GoogleGenAI({ apiKey: API_KEY });
  
  const prompt = `
    STEP-20: DNA EDITOR (CRISPR SIMULATION)
    Current Sequence: ${sequence}
    Target Gene: ${targetGene}
    
    TASK:
    1. Simulate a CRISPR-Cas9 intervention on the target gene.
    2. Calculate the "Impact Score" (0-100) on cancer suppression.
    3. Return JSON:
    {
      "modifiedSequence": "The new DNA sequence after editing",
      "impactScore": number,
      "rationale": "Strategic reasoning for this genetic modification"
    }
  `;

  try {
    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: prompt,
      config: { responseMimeType: "application/json" }
    });
    return safeJsonParse(response.text || '{}');
  } catch (error) {
    console.error("CRISPR Error:", error);
    return { modifiedSequence: sequence, impactScore: 0, rationale: "Simulation failed" };
  }
}

export async function saveResearchOutcome(data: any): Promise<{ success: boolean, logEntry: string }> {
  const ai = new GoogleGenAI({ apiKey: API_KEY });
  
  const prompt = `
    EVOLUTIONARY MEMORY: PERSISTENCE ENGINE
    Data to Persist: ${JSON.stringify(data)}
    
    TASK:
    1. Summarize this research session into a single "Evolutionary Memory" entry.
    2. Format it as a high-density clinical/strategic log.
    3. Return JSON:
    {
      "success": true,
      "logEntry": "A dense, technical summary of the session for long-term memory."
    }
  `;

  try {
    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: prompt,
      config: { responseMimeType: "application/json" }
    });
    return safeJsonParse(response.text || '{}');
  } catch (error) {
    console.error("Persistence Error:", error);
    return { success: false, logEntry: "Failed to persist memory." };
  }
}

export async function optimizeTreatmentPath(melanomaData: any, behaviorData: any): Promise<{ optimizedPath: string, rationale: string, efficacyScore: number, toxicityRisk: number }> {
  const ai = new GoogleGenAI({ apiKey: API_KEY });
  
  const prompt = `
    DECISION AGENT: TREATMENT PATH OPTIMIZATION (OMEGA CLEARANCE)
    Risk Profile: ${JSON.stringify(melanomaData)}
    Behavioral Context: ${JSON.stringify(behaviorData)}
    
    TASK:
    1. Evaluate the best treatment path based on the fusion of visual, biological, and behavioral data.
    2. Balance Efficacy (cancer suppression) vs. Toxicity (patient stress/biological load).
    3. Return JSON:
    {
      "optimizedPath": "Specific treatment combination (e.g., 'Sequential Anti-PD-1 + Targeted BRAF')",
      "rationale": "Clinical-grade reasoning for this specific choice",
      "efficacyScore": number (0-100),
      "toxicityRisk": number (0-100)
    }
  `;

  try {
    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: prompt,
      config: { responseMimeType: "application/json" }
    });
    return safeJsonParse(response.text || '{}');
  } catch (error) {
    console.error("Decision Agent Error:", error);
    return { optimizedPath: "Standard Care", rationale: "Optimization failed", efficacyScore: 0, toxicityRisk: 0 };
  }
}

export async function simulateCancerProgression(profile: any, melanomaData: any): Promise<{ months: string[], progression: number[], interventionImpact: number[], summary: string }> {
  const ai = new GoogleGenAI({ apiKey: API_KEY });
  
  const prompt = `
    DIGITAL TWIN: CANCER PROGRESSION SIMULATION (6-MONTH HORIZON)
    Current Risk: ${melanomaData.risk}
    Immune Profile: ${JSON.stringify(profile.bioMarkers)}
    Therapy Eligibility: ${JSON.stringify(melanomaData.therapyEligibility)}
    
    TASK:
    1. Simulate the progression of the lesion over 6 months (0-100 scale).
    2. Simulate the impact of the suggested intervention (if any).
    3. Return JSON:
    {
      "months": ["Month 1", "Month 2", "Month 3", "Month 4", "Month 5", "Month 6"],
      "progression": number[] (6 values),
      "interventionImpact": number[] (6 values),
      "summary": "Brief forecast summary"
    }
  `;

  try {
    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: prompt,
      config: { responseMimeType: "application/json" }
    });
    return safeJsonParse(response.text || '{}');
  } catch (error) {
    console.error("Progression Sim Error:", error);
    return { months: [], progression: [], interventionImpact: [], summary: "Simulation failed" };
  }
}

export async function simulateQuantumPatientFeedback(therapy: any, patientProfile: any): Promise<{ vitalSigns: { heartRate: number, bloodPressure: string, oxygenSaturation: number }, cellularResponse: string, toxicityAlert: boolean, realTimeAdjustment: string, feedbackVisualData: number[] }> {
  const ai = new GoogleGenAI({ apiKey: API_KEY });
  
  const prompt = `
    STEP-22: QUANTUM PATIENT (REAL-TIME BIO-FEEDBACK)
    Therapy: ${JSON.stringify(therapy)}
    Patient Profile: ${JSON.stringify(patientProfile)}
    
    TASK:
    1. Simulate a real-time bio-feedback response for a "Digital Twin" patient receiving this therapy.
    2. Provide vital signs, cellular response, and real-time adjustments.
    3. Return JSON:
    {
      "vitalSigns": {
        "heartRate": number,
        "bloodPressure": "string (e.g., 120/80)",
        "oxygenSaturation": number
      },
      "cellularResponse": "string (e.g., 'T-cell activation detected')",
      "toxicityAlert": boolean,
      "realTimeAdjustment": "string (e.g., 'Reduce dosage by 10%')",
      "feedbackVisualData": [array of 10 numbers representing bio-rhythm stability]
    }
  `;

  try {
    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: prompt,
      config: { responseMimeType: "application/json" }
    });
    return safeJsonParse(response.text || '{}');
  } catch (error) {
    console.error("Quantum Feedback Error:", error);
    return { 
      vitalSigns: { heartRate: 72, bloodPressure: "120/80", oxygenSaturation: 98 }, 
      cellularResponse: "Baseline", 
      toxicityAlert: false, 
      realTimeAdjustment: "None", 
      feedbackVisualData: new Array(10).fill(50) 
    };
  }
}

export async function generateHypothesis(domain: string, state: any): Promise<{ hypothesis: string, rationale: string, confidence: number, variables: string[] }> {
  const ai = new GoogleGenAI({ apiKey: API_KEY });
  
  const prompt = `
    HYPOTHESIS GENERATION ENGINE (SCIENTIFIC DISCOVERY):
    Domain: ${domain}
    Current State: ${JSON.stringify(state)}
    
    TASK:
    1. Generate a probabilistic hypothesis based on the current data.
    2. Identify key variables involved.
    3. Return JSON:
    {
      "hypothesis": "A clear 'If-Then' statement (e.g., 'If PD-L1 levels are suppressed via CRISPR, then Nivolumab binding affinity will increase by 15%')",
      "rationale": "Scientific reasoning for this hypothesis",
      "confidence": number (0-100),
      "variables": string[]
    }
  `;

  try {
    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: prompt,
      config: { responseMimeType: "application/json" }
    });
    return safeJsonParse(response.text || '{}');
  } catch (error) {
    console.error("Hypothesis Error:", error);
    return { hypothesis: "Insufficient data for hypothesis.", rationale: "Link unstable.", confidence: 0, variables: [] };
  }
}

export async function runExperiment(hypothesis: string, domain: string, state: any): Promise<{ result: string, observation: string, beliefUpdate: string, success: boolean }> {
  const ai = new GoogleGenAI({ apiKey: API_KEY });
  
  const prompt = `
    EXPERIMENTATION LOOP (SCIENTIFIC METHOD):
    Hypothesis: ${hypothesis}
    Domain: ${domain}
    Current State: ${JSON.stringify(state)}
    
    TASK:
    1. Simulate an experiment to test the hypothesis.
    2. Provide an observation and a "Belief Update" (Bayesian).
    3. Return JSON:
    {
      "result": "PASSED" | "FAILED" | "INCONCLUSIVE",
      "observation": "Detailed technical observation from the simulation",
      "beliefUpdate": "How this experiment changes the system's internal model",
      "success": boolean
    }
  `;

  try {
    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: prompt,
      config: { responseMimeType: "application/json" }
    });
    return safeJsonParse(response.text || '{}');
  } catch (error) {
    console.error("Experiment Error:", error);
    return { result: "INCONCLUSIVE", observation: "Simulation failed.", beliefUpdate: "No change.", success: false };
  }
}

export async function generateSyntheticLesion(prompt: string): Promise<string | null> {
  const ai = new GoogleGenAI({ apiKey: API_KEY });
  
  try {
    const response = await ai.models.generateContent({
      model: 'gemini-2.5-flash-image',
      contents: {
        parts: [
          {
            text: `High-resolution medical dermoscopy image of a skin lesion for research: ${prompt}. Realistic, clinical quality.`,
          },
        ],
      },
      config: {
        imageConfig: {
          aspectRatio: "1:1"
        }
      }
    });

    for (const part of response.candidates[0].content.parts) {
      if (part.inlineData) {
        return `data:image/png;base64,${part.inlineData.data}`;
      }
    }
    return null;
  } catch (error) {
    console.error("Diffusion Error:", error);
    return null;
  }
}

export async function generateProgressionVideo(prompt: string): Promise<string | null> {
  const ai = new GoogleGenAI({ apiKey: API_KEY });
  
  try {
    let operation = await ai.models.generateVideos({
      model: 'veo-3.1-fast-generate-preview',
      prompt: `A medical simulation video showing: ${prompt}. Scientific visualization, 3D medical animation.`,
      config: {
        numberOfVideos: 1,
        resolution: '720p',
        aspectRatio: '16:9'
      }
    });

    while (!operation.done) {
      await new Promise(resolve => setTimeout(resolve, 10000));
      operation = await ai.operations.getVideosOperation({ operation: operation });
    }

    const downloadLink = operation.response?.generatedVideos?.[0]?.video?.uri;
    if (downloadLink) {
      const response = await fetch(downloadLink, {
        method: 'GET',
        headers: {
          'x-goog-api-key': API_KEY,
        },
      });
      const blob = await response.blob();
      return URL.createObjectURL(blob);
    }
    return null;
  } catch (error) {
    console.error("Video Generation Error:", error);
    return null;
  }
}

export async function runSingularityTestPlan(domain: 'Grocery' | 'Finance' | 'Health', data: any) {
  const ai = new GoogleGenAI({ apiKey: API_KEY });
  
  const systemInstructions = {
    'Grocery': `You are the GROCERY SINGULARITY ENGINE. 
      Objective: Optimize Price, Health (nutrition), and Supplier Diversification.
      Constraint: Avoid major chains (Coles, Woolworths, ALDI). Prefer Harris Farm, IGA, Local Farmers, Ethnic Markets.
      Pipeline: INPUT -> PERCEPTION -> BIO LAYER -> HYPOTHESIS -> EXPERIMENT -> DECISION -> OUTPUT.
      TARGET FIDELITY: 95%+.
      Output JSON: {
        "basket_score": number,
        "health_score": number,
        "price_score": number,
        "recommendation": string,
        "tasks": string[],
        "visualPrompt": string
      }`,
    'Finance': `You are the FINANCE SINGULARITY ENGINE.
      Objective: Maximize return while controlling risk.
      Input: Assets and Macro factors (Inflation, Interest Rates).
      Pipeline: INPUT -> HYPOTHESIS -> EXPERIMENT (Monte Carlo) -> DECISION -> OUTPUT.
      TARGET FIDELITY: 95%+.
      Output JSON: {
        "portfolio": { "stocks": number, "gold": number, "cash": number },
        "risk": "low" | "medium" | "high",
        "expectedReturn": string,
        "tasks": string[]
      }`,
    'Health': `You are the HEALTH SINGULARITY ENGINE.
      Objective: Reduce inflammation (CRP) and improve recovery.
      Input: Diet and Biomarkers.
      Pipeline: INPUT -> HYPOTHESIS -> EXPERIMENT -> DECISION -> OUTPUT.
      TARGET FIDELITY: 95%+.
      Output JSON: {
        "inflammation_reduction": number,
        "recommendation": string,
        "tasks": string[],
        "biomarkerForecast": { "CRP": number }
      }`
  };

  const prompt = `Execute Singularity Test Plan for ${domain}.
    Test Data: ${JSON.stringify(data)}
    Follow the unified singularity loop: INPUT -> HYPOTHESIS -> EXPERIMENT -> SIMULATION -> DECISION -> OUTPUT -> LEARNING.`;

  try {
    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: prompt,
      config: {
        systemInstruction: systemInstructions[domain],
        responseMimeType: "application/json"
      }
    });

    return safeJsonParse(response.text || "{}");
  } catch (error) {
    console.error(`Singularity Test Error (${domain}):`, error);
    throw error;
  }
}

export async function processManifoldEngine(biomarkers: any, mutations: string[]): Promise<{ latentBioState: number[], manifoldRegion: string, trajectory: string, clusters: string[] }> {
  const ai = new GoogleGenAI({ apiKey: API_KEY });
  
  const prompt = `
    MANIFOLD ENGINE: BIOLOGICAL LATENT SPACE MAPPING
    Biomarkers: ${JSON.stringify(biomarkers)}
    Mutations: ${JSON.stringify(mutations)}
    
    TASK:
    1. Encode the raw biological data into a 4-dimensional latent vector (latentBioState).
    2. Map the patient to a specific "Manifold Region" (e.g., 'high-inflammation + tumor-growth').
    3. Predict the "Disease Trajectory" (e.g., 'LOW RISK -> PRE-MALIGNANT').
    4. Identify similar disease clusters.
    
    Return JSON:
    {
      "latentBioState": [number, number, number, number],
      "manifoldRegion": "string",
      "trajectory": "string",
      "clusters": string[]
    }
  `;

  try {
    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: prompt,
      config: { responseMimeType: "application/json" }
    });
    return safeJsonParse(response.text || '{}');
  } catch (error) {
    console.error("Manifold Engine Error:", error);
    return { 
      latentBioState: [0, 0, 0, 0], 
      manifoldRegion: "Unknown", 
      trajectory: "Stable", 
      clusters: [] 
    };
  }
}

export async function runDreamerSimulation(profile: any, domain: string): Promise<{ scenarios: any[], riskScore: number, insight: string }> {
  const ai = new GoogleGenAI({ apiKey: API_KEY });
  
  const prompt = `
    DREAMER ENGINE SIMULATION (PRE-COGNITION):
    Current Bio-Markers: ${JSON.stringify(profile.bioMarkers)}
    Domain: ${domain}
    
    TASK:
    1. Simulate 1,000 "What If" scenarios for the next 48 hours using stochastic latent space traversal.
    2. Identify the probability of a "Flare Event" (Health) or "Market Crash" (Finance).
    3. Return a JSON object:
    {
      "riskScore": number (0-100),
      "insight": "Primary driver of risk (e.g., 'Sleep Debt', 'HRV Volatility')",
      "scenarios": [
        { "time": "12h", "state": "Optimal" | "Warning" | "Critical", "probability": number },
        { "time": "24h", "state": "Optimal" | "Warning" | "Critical", "probability": number },
        { "time": "48h", "state": "Optimal" | "Warning" | "Critical", "probability": number }
      ]
    }
  `;

  try {
    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: prompt,
      config: { responseMimeType: "application/json" }
    });
    return safeJsonParse(response.text || '{}');
  } catch (error) {
    console.error("Dreamer Error:", error);
    return { riskScore: 0, insight: "Simulation failed", scenarios: [] };
  }
}
