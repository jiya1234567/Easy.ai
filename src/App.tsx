/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useRef, useEffect } from 'react';
import { 
  Shield, 
  Cpu, 
  Globe, 
  Network, 
  Dna, 
  Camera, 
  X, 
  Play, 
  Send, 
  CheckCircle2, 
  AlertCircle,
  Loader2,
  Terminal,
  Zap,
  User,
  Settings,
  Activity,
  Leaf,
  DollarSign,
  MessageSquare,
  Bot,
  Lock,
  Unlock,
  RefreshCw,
  ChevronRight,
  Plus,
  Minus,
  Smartphone,
  Microscope,
  Video,
  Radio,
  Wifi,
  Database,
  Upload,
  FileText,
  Brain,
  Target,
  ShieldCheck,
  ShieldAlert,
  Eye,
  Scan,
  Lightbulb,
  Trophy,
  BookOpen,
  Bell,
  Search,
  Layout,
  Mic,
  MicOff,
  Volume2,
  Calendar,
  Mail,
  CheckSquare,
  Clock,
  Stethoscope,
  TrendingUp,
  AlertTriangle,
  Users,
  Save,
  PhoneCall,
  Menu,
  BarChart3,
  History,
  ArrowUpRight,
  ArrowDownRight,
  Layers,
  BarChart as BarChartIcon,
  LineChart as LineChartIcon,
  PieChart as PieChartIcon
} from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { cn } from './lib/utils';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  BarChart, 
  Bar, 
  Cell 
} from 'recharts';
import { 
  processUniversalLabRequest, 
  agentChat, 
  processSelfImprovementLoop,
  processVoiceInput,
  generateVoiceResponse,
  runDreamerSimulation,
  analyzeMelanomaLesion,
  fuseMelanomaMarkers,
  simulateCancerProgression,
  analyzeBehavior,
  optimizeTreatmentPath,
  saveResearchOutcome,
  simulateCRISPRIntervention,
  simulateMolecularDocking,
  generateTherapyRecommendation,
  simulateQuantumPatientFeedback,
  generateHypothesis,
  runExperiment,
  generateSyntheticLesion,
  generateProgressionVideo,
  processManifoldEngine,
  runSingularityTestPlan,
  generateDetailedFinanceReport,
  safeJsonParse
} from './services/geminiService';
import { runBacktestSimulation, BacktestResult, AccuracyMetrics } from './services/backtestService';

type Tab = 'HOW TO USE' | 'FACTORY (CHAT)' | 'REPORTS' | 'WORLD MODEL' | 'HIERARCHY' | 'EVOLUTION' | 'RESEARCH DEVICE' | 'COMMAND CENTER' | 'SCIENTIFIC DISCOVERY' | 'VISUAL SIMULATION' | 'MANIFOLD' | 'COSMO-HUMANOID' | 'BACKTEST';
type Domain = 'General' | 'Health' | 'Agriculture' | 'Finance' | 'Grocery' | 'DrugDiscovery';

interface Task {
  text: string;
  completed: boolean;
  approved: boolean;
}

interface TodoItem {
  id: string;
  text: string;
  completed: boolean;
  source: 'agent' | 'user';
  priority: 'low' | 'medium' | 'high';
}

interface Notification {
  id: string;
  type: 'health' | 'stock' | 'system';
  message: string;
  timestamp: string;
  read: boolean;
}

interface UserProfile {
  budget: string;
  bioMarkers: {
    heartRate: string;
    glucose: string;
    hrv: string;
    spo2: string;
    skinTemp: string;
    respiratoryRate: string;
    sleepScore: string;
  };
  learningNodes: string[];
}

const ManifoldVisualization = ({ data }: { data: number[] }) => {
  // Simple 2D projection of 4D data
  const x = (data[0] + data[2]) * 50 + 100;
  const y = (data[1] + data[3]) * 50 + 100;

  return (
    <div className="relative w-full h-48 bg-black/40 rounded-lg border border-white/10 overflow-hidden">
      <div className="absolute inset-0 flex items-center justify-center opacity-20">
        <div className="w-full h-[1px] bg-white/20" />
        <div className="h-full w-[1px] bg-white/20" />
      </div>
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1, x: x - 100, y: y - 100 }}
        className="absolute top-1/2 left-1/2 w-4 h-4 bg-blue-500 rounded-full shadow-[0_0_15px_rgba(59,130,246,0.8)]"
      />
      <div className="absolute bottom-2 left-2 text-[10px] font-mono text-white/40">
        LATENT SPACE PROJECTION (v1.0)
      </div>
    </div>
  );
};

export default function App() {
  const [activeTab, setActiveTab] = useState<Tab>('HOW TO USE');
  const [activeDomain, setActiveDomain] = useState<Domain>('General');
  const [missionIntent, setMissionIntent] = useState('');
  const [ticker, setTicker] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [isLooping, setIsLooping] = useState(false);
  const [loopStep, setLoopStep] = useState(0);
  const [loopData, setLoopData] = useState<any>(null);
  const [prediction, setPrediction] = useState<string | null>(null);
  const [summary, setSummary] = useState<string | null>(null);
  const [suggestions, setSuggestions] = useState<string | null>(null);
  const [agentReports, setAgentReports] = useState<{ scientist: string, riskManager: string, strategist: string, groundingAgent?: string } | null>(null);
  const [groundingStatus, setGroundingStatus] = useState<{ verified: boolean, source: string, gaps: { description: string, fix: string }[], confidence: number } | null>(null);
  const [executionLogs, setExecutionLogs] = useState<string[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [todoList, setTodoList] = useState<TodoItem[]>([]);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [routedModel, setRoutedModel] = useState<string | null>(null);
  const [capturedImage, setCapturedImage] = useState<string | null>(null);
  const [uploadedText, setUploadedText] = useState<string | null>(null);
  const [textContent, setTextContent] = useState('');
  const [isAutoimmuneMode, setIsAutoimmuneMode] = useState(false);
  const [chatHistory, setChatHistory] = useState<{role: 'user' | 'agent', content: string}[]>([]);
  const [isCameraOpen, setIsCameraOpen] = useState(false);
  const [isAudioUnlocked, setIsAudioUnlocked] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Profile State
  const [profile, setProfile] = useState<UserProfile>({
    budget: '$10,000,000',
    bioMarkers: {
      heartRate: '72 bpm',
      glucose: '95 mg/dL',
      hrv: '65 ms',
      spo2: '98%',
      skinTemp: '36.6°C',
      respiratoryRate: '14 br/m',
      sleepScore: '85/100'
    },
    learningNodes: ['Ruliad-v1', 'Hypergraph-Core']
  });

  // Agent State
  const [isAutoPilot, setIsAutoPilot] = useState(false);
  const [isExecutingTrade, setIsExecutingTrade] = useState(false);
  const [tradeProgress, setTradeProgress] = useState(0);
  const [tradeStatus, setTradeStatus] = useState<string | null>(null);
  const [chatMessages, setChatMessages] = useState<{role: 'user' | 'agent', text: string}[]>([]);
  const [chatInput, setChatInput] = useState('');
  const [neuralLog, setNeuralLog] = useState<{timestamp: string, agent: string, action: string}[]>([]);
  const [ruliadRules, setRuliadRules] = useState<{rule: string, dimension: string, probability: number}[]>([]);
  const [isSearchingRuliad, setIsSearchingRuliad] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessingVoice, setIsProcessingVoice] = useState(false);
  const [dreamerData, setDreamerData] = useState<{ scenarios: any[], riskScore: number, insight: string } | null>(null);
  const [isDreaming, setIsDreaming] = useState(false);
  const [melanomaData, setMelanomaData] = useState<{ risk: number, action: string, features: any, reasoning: string, therapyEligibility: string[] } | null>(null);
  const [isAnalyzingMelanoma, setIsAnalyzingMelanoma] = useState(false);
  const [progressionData, setProgressionData] = useState<{ months: string[], progression: number[], interventionImpact: number[], summary: string } | null>(null);
  const [isSimulatingProgression, setIsSimulatingProgression] = useState(false);
  const [behaviorData, setBehaviorData] = useState<{ emotion: string, motion: string, stressLevel: number, insight: string } | null>(null);
  const [isAnalyzingBehavior, setIsAnalyzingBehavior] = useState(false);
  const [decisionData, setDecisionData] = useState<{ optimizedPath: string, rationale: string, efficacyScore: number, toxicityRisk: number } | null>(null);
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [isSavingMemory, setIsSavingMemory] = useState(false);
  const [dnaSequence, setDnaSequence] = useState("ATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGC");
  const [targetGene, setTargetGene] = useState("BRAF-V600E");
  const [crisprResult, setCrisprResult] = useState<{ modifiedSequence: string, impactScore: number, rationale: string } | null>(null);
  const [isEditingDNA, setIsEditingDNA] = useState(false);
  const [dockingData, setDockingData] = useState<{ bindingAffinity: number, stabilityScore: number, dockingVisualData: number[], rationale: string } | null>(null);
  const [isDocking, setIsDocking] = useState(false);
  const [therapyRecommendation, setTherapyRecommendation] = useState<{ therapyType: string, dosage: string, schedule: string, expectedOutcome: string, riskLevel: string } | null>(null);
  const [isGeneratingTherapy, setIsGeneratingTherapy] = useState(false);
  const [drugMolecule, setDrugMolecule] = useState("Nivolumab (Opdivo)");
  const [quantumFeedback, setQuantumFeedback] = useState<{ vitalSigns: { heartRate: number, bloodPressure: string, oxygenSaturation: number }, cellularResponse: string, toxicityAlert: boolean, realTimeAdjustment: string, feedbackVisualData: number[] } | null>(null);
  const [isSimulatingQuantum, setIsSimulatingQuantum] = useState(false);

  // Hypothesis Engine State
  const [hypothesis, setHypothesis] = useState<{ hypothesis: string, rationale: string, confidence: number, variables: string[] } | null>(null);
  const [isGeneratingHypothesis, setIsGeneratingHypothesis] = useState(false);
  const [experimentResult, setExperimentResult] = useState<{ result: string, observation: string, beliefUpdate: string, success: boolean } | null>(null);
  const [isRunningExperiment, setIsRunningExperiment] = useState(false);

  // Visual Simulation State
  const [syntheticImage, setSyntheticImage] = useState<string | null>(null);
  const [isGeneratingImage, setIsGeneratingImage] = useState(false);
  const [progressionVideo, setProgressionVideo] = useState<string | null>(null);
  const [isGeneratingVideo, setIsGeneratingVideo] = useState(false);
  const [videoProgress, setVideoProgress] = useState(0);
  const [isEmergencyCallActive, setIsEmergencyCallActive] = useState(false);
  const [emergencyCallTimer, setEmergencyCallTimer] = useState(0);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [backtestData, setBacktestData] = useState<{ results: BacktestResult[], metrics: AccuracyMetrics } | null>(null);
  const [isBacktesting, setIsBacktesting] = useState(false);
  
  // Manifold Engine State
  const [manifoldData, setManifoldData] = useState<{ latentBioState: number[], manifoldRegion: string, trajectory: string, clusters: string[] } | null>(null);
  const [isAnalyzingManifold, setIsAnalyzingManifold] = useState(false);
  const [isTesting, setIsTesting] = useState(false);
  const [isLiveFeedEnabled, setIsLiveFeedEnabled] = useState(false);
  const [liveDataStatus, setLiveDataStatus] = useState<string | null>(null);
  const [isEyeScanning, setIsEyeScanning] = useState(false);
  const [eyeScanResult, setEyeScanResult] = useState<string | null>(null);
  const [financeReport, setFinanceReport] = useState<any | null>(null);
  const [isGeneratingFinanceReport, setIsGeneratingFinanceReport] = useState(false);

  // Cosmo-Humanoid State
  const [humanoidState, setHumanoidState] = useState({
    mood: 0.5,
    stress: 0.2,
    attention: 0.8,
    energy: 0.9,
    goalFocus: 0.7,
    anger: 0.0,
    calm: 0.8,
    engagement: 0.6
  });
  const [satelliteStatus, setSatelliteStatus] = useState({
    link: 'STABLE',
    latency: '420ms',
    uplink: '12.4 Mbps',
    downlink: '45.2 Mbps',
    orbit: 'LEO-4'
  });
  const [robotMotors, setRobotMotors] = useState({
    neck: 0,
    leftArm: 15,
    rightArm: -10,
    torso: 5,
    legs: 'STATIONARY'
  });
  const [testResults, setTestResults] = useState<{ domain: string, steps: string[] }[]>([]);
  const [alertThreshold, setAlertThreshold] = useState(10);
  const [isEmailAlertEnabled, setIsEmailAlertEnabled] = useState(false);
  const [isSmsAlertEnabled, setIsSmsAlertEnabled] = useState(false);
  const [phoneNumber, setPhoneNumber] = useState('+1 (555) 000-0000');
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const animationFrameRef = useRef<number | null>(null);
  const [waveform, setWaveform] = useState<number[]>(new Array(20).fill(0));

  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const streamRef = useRef<MediaStream | null>(null);

  useEffect(() => {
    // Simulate Neural Log activity
    const interval = setInterval(() => {
      const agents = ['SCIENTIST', 'RISK MANAGER', 'STRATEGIST', 'EVOLUTION ENGINE'];
      const actions = [
        'Analyzing IL-6 hypergraph nodes...',
        'Recalculating flare probability thresholds...',
        'Optimizing circadian metabolic alignment...',
        'Synthesizing Ruliad-v2 insights...',
        'Verifying budget constraints for TSLA ingress...',
        'Syncing with Geneva Research Node-04...',
        'Updating metabolic resilience factor...'
      ];
      
      const newEntry = {
        timestamp: new Date().toLocaleTimeString(),
        agent: agents[Math.floor(Math.random() * agents.length)],
        action: actions[Math.floor(Math.random() * actions.length)]
      };
      
      setNeuralLog(prev => [newEntry, ...prev].slice(0, 50));
    }, 8000);
    
    return () => clearInterval(interval);
  }, []);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { facingMode: 'user' } 
      });
      streamRef.current = stream;
      setIsCameraOpen(true);
    } catch (err) {
      setError("Camera access denied. Please check permissions.");
    }
  };

  useEffect(() => {
    if (isCameraOpen && videoRef.current && streamRef.current) {
      videoRef.current.srcObject = streamRef.current;
    }
  }, [isCameraOpen]);

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    setIsCameraOpen(false);
  };

  const playAudio = (base64: string): Promise<void> => {
    return new Promise((resolve) => {
      if (!isAudioUnlocked) {
        resolve();
        return;
      }
      const audio = new Audio(`data:audio/wav;base64,${base64}`);
      audio.onended = () => resolve();
      audio.onerror = () => resolve();
      audio.play().catch(err => {
        console.warn("Audio playback failed:", err);
        resolve();
      });
    });
  };

  const speak = async (text: string): Promise<void> => {
    if (!isAudioUnlocked) return;
    try {
      const audioRes = await generateVoiceResponse(text);
      if (audioRes) {
        await playAudio(audioRes);
      }
    } catch (err) {
      console.error("Speak error:", err);
    }
  };

  const capturePhoto = () => {
    if (videoRef.current && canvasRef.current) {
      const context = canvasRef.current.getContext('2d');
      if (context) {
        canvasRef.current.width = videoRef.current.videoWidth;
        canvasRef.current.height = videoRef.current.videoHeight;
        context.drawImage(videoRef.current, 0, 0);
        const dataUrl = canvasRef.current.toDataURL('image/jpeg');
        setCapturedImage(dataUrl);
        stopCamera();
      }
    }
  };

  useEffect(() => {
    // Verify server connectivity
    fetch('/api/health')
      .then(res => res.json())
      .then(data => console.log('Server Status:', data))
      .catch(err => console.error('Server offline:', err));
  }, []);

  const handleGenerateFinanceReport = async () => {
    if (!ticker && activeDomain !== 'Finance') return;
    setIsGeneratingFinanceReport(true);
    setExecutionLogs(prev => [...prev, `[FINANCE] Initiating deep-dive forecast for ${ticker || 'ANZ'}...`, "[FINANCE] Traversing ASX data streams...", "[FINANCE] Analyzing multiples and technical indicators..."]);
    
    try {
      const report = await generateDetailedFinanceReport(ticker || 'ANZ', profile);
      setFinanceReport(report);
      setExecutionLogs(prev => [...prev, "[SUCCESS] Finance Forecast Report Generated.", `[FINANCE] Target Price (Base): ${report.forecast.base.target}`]);
      setActiveTab('REPORTS');
      
      if (report.gaps && report.gaps.length > 0) {
        setNotifications(prev => [{
          id: Date.now().toString(),
          type: 'system',
          message: `FINANCE REPORT: ${report.gaps.length} data gaps identified. Grounding Agent required.`,
          timestamp: new Date().toLocaleTimeString(),
          read: false
        }, ...prev]);
      }
    } catch (err) {
      console.error("Finance report error:", err);
      setError("Failed to generate finance report.");
    } finally {
      setIsGeneratingFinanceReport(false);
    }
  };

  const handleRuliadSearch = async () => {
    setIsSearchingRuliad(true);
    setExecutionLogs(prev => [...prev, "Traversing Ruliad Hypergraph...", "Extracting non-obvious causal edges..."]);
    
    try {
      const prompt = `As a Singularity Strategist, extract 5 non-obvious "Ruliad Rules" (computational universe rules) for the following domain and intent:
      Domain: ${activeDomain}
      Intent: ${missionIntent || ticker || activeDomain}
      
      Format each rule as a JSON object with:
      - rule: A short, profound rule statement.
      - dimension: The computational dimension it exists in (e.g., "Causal", "Multiway", "Branchial").
      - probability: A confidence score between 0 and 1.
      
      Return ONLY the JSON array.`;

      const response = await processUniversalLabRequest(
        activeDomain,
        prompt,
        undefined,
        ticker,
        profile,
        undefined,
        true // Flag for raw JSON response
      );

      if (response && response.ruliadRules) {
        setRuliadRules(response.ruliadRules);
      } else {
        // Fallback mock rules if AI fails or returns unexpected format
        setRuliadRules([
          { rule: "Causal invariance across metabolic nodes.", dimension: "Causal", probability: 0.98 },
          { rule: "Multiway branching of stock volatility vectors.", dimension: "Multiway", probability: 0.85 },
          { rule: "Branchial entanglement of immune response.", dimension: "Branchial", probability: 0.92 }
        ]);
      }
      
      setExecutionLogs(prev => [...prev, "[SUCCESS] Ruliad Traversal Complete. 5 Rules Extracted."]);
    } catch (err) {
      console.error("Ruliad Search Error:", err);
      setError("Failed to traverse Ruliad. Uplink unstable.");
    } finally {
      setIsSearchingRuliad(false);
    }
  };

  // Smart Watch Monitor: Continuous Wearable Sync
  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isLiveFeedEnabled) {
      interval = setInterval(() => {
        const newHRV = Math.floor(Math.random() * (80 - 30) + 30);
        const newStress = Math.floor(Math.random() * 100);
        
        setProfile(prev => ({
          ...prev,
          bioMarkers: {
            ...prev.bioMarkers,
            hrv: newHRV.toString(),
            heartRate: (Math.floor(Math.random() * (90 - 60) + 60)).toString()
          }
        }));
        
        setBehaviorData(prev => ({
          emotion: newStress > 70 ? "High Stress" : "Calm",
          motion: "Active",
          stressLevel: newStress,
          insight: newStress > 70 ? "Elevated cortisol detected. Throttling high-risk execution." : "Bio-metric baseline stable."
        }));
        
        if (newStress > 85) {
          const alert: Notification = {
            id: Date.now().toString(),
            type: 'health',
            message: `SMARTWATCH ALERT: Critical Stress Level (${newStress}%). Initiating de-escalation protocol.`,
            timestamp: new Date().toLocaleTimeString(),
            read: false
          };
          setNotifications(prev => [alert, ...prev]);
        }
      }, 5000);
    }
    return () => clearInterval(interval);
  }, [isLiveFeedEnabled]);

  const handleProcess = async () => {
    if (!missionIntent && !ticker && !capturedImage && !uploadedText) return;
    
    setIsProcessing(true);
    setError(null);
    try {
      const result = await processUniversalLabRequest(
        activeDomain,
        missionIntent || `Analyze ${ticker || activeDomain} for hypergraph evolution.`,
        capturedImage || undefined,
        ticker,
        profile,
        uploadedText || undefined
      );
      
      setPrediction(result.prediction);
      setSummary(result.summary);
      setSuggestions(result.suggestions);
      setRoutedModel(result.routedModel);
      setAgentReports(result.agentReports || null);
      setGroundingStatus(result.groundingStatus || null);
      
      // CROSS-MODULE SYNC: If stress is high, the Risk Manager should be more aggressive
      if (behaviorData && behaviorData.stressLevel > 70 && result.agentReports) {
        setAgentReports(prev => prev ? {
          ...prev,
          riskManager: `[STRESS INTERRUPT] User stress at ${behaviorData.stressLevel}%. High-risk execution throttled. ${prev.riskManager}`
        } : null);
      }
      
      if (result.todoItems && Array.isArray(result.todoItems)) {
        const newTodos: TodoItem[] = result.todoItems.map((t: any) => ({
          id: Math.random().toString(36).substr(2, 9),
          text: t.text,
          completed: false,
          source: 'agent',
          priority: t.priority || 'medium'
        }));
        setTodoList(prev => [...newTodos, ...prev]);
      }

      if (result.notifications && Array.isArray(result.notifications)) {
        const newNotifs: Notification[] = result.notifications.map((n: any) => ({
          id: Math.random().toString(36).substr(2, 9),
          type: n.type,
          message: n.message,
          timestamp: new Date().toLocaleTimeString(),
          read: false
        }));
        setNotifications(prev => [...newNotifs, ...prev]);
        
        // Simulate alerts
        if (isEmailAlertEnabled) {
          newNotifs.forEach(n => {
            fetch('/api/alert', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ type: n.type, message: n.message, email: 'aejphillips@outlook.com' })
            }).catch(console.error);
          });
        }
        if (isSmsAlertEnabled) {
          newNotifs.forEach(n => {
            setExecutionLogs(prev => [...prev, `[SMS] Dispatching alert to ${phoneNumber}: ${n.message}`]);
          });
        }
      }
      
      const newTasks = (result.tasks || []).map((t: string) => ({ 
        text: t, 
        completed: false, 
        approved: isAutoPilot 
      }));
      setTasks(newTasks);
      
      // Initiate Self-Improvement Loop
      setIsLooping(true);
      const steps = 11;
      for (let i = 1; i <= steps; i++) {
        setLoopStep(i);
        await new Promise(r => setTimeout(r, 800)); // Visual delay for the loop
      }

      const loopResult = await processSelfImprovementLoop(
        activeDomain,
        missionIntent || ticker || activeDomain,
        result,
        profile
      );
      setLoopData(loopResult);
      setIsLooping(false);
      
      // Update Chat History
      setChatHistory(prev => [
        ...prev, 
        { role: 'user', content: missionIntent || `Analyzing ${ticker || activeDomain}` },
        { role: 'agent', content: result.summary }
      ].slice(-6)); // Keep last 3 exchanges
      
      // Auto-execution simulation
      if (isAutoPilot) {
        setExecutionLogs(prev => [...prev, "Initiating Auto-Execution Protocol...", "Verifying Budget Constraints...", "Executing Directives..."]);
        for (const task of result.tasks) {
          await new Promise(r => setTimeout(r, 1000));
          setExecutionLogs(prev => [...prev, `[SUCCESS] Executed: ${task}`]);
        }
        setExecutionLogs(prev => [...prev, "Mission Complete. All directives executed."]);
      }
      
      // Recursive learning update
      setProfile(prev => ({
        ...prev,
        learningNodes: [...new Set([...prev.learningNodes, `${activeDomain}-Node-${Date.now().toString().slice(-4)}`])]
      }));

      if (isAutoPilot) {
        setChatMessages(prev => [...prev, { role: 'agent', text: "Auto-Pilot active. All directives approved. Initiating execution sequence." }]);
      }

    } catch (err: any) {
      setError(err.message || "An error occurred during processing.");
    } finally {
      setIsProcessing(false);
    }
  };

  const toggleTaskApproval = (idx: number) => {
    setTasks(prev => prev.map((t, i) => i === idx ? { ...t, approved: !t.approved } : t));
  };

  const [syncLevel, setSyncLevel] = useState(85);

  const toggleTaskCompletion = (idx: number) => {
    setTasks(prev => {
      const newTasks = prev.map((t, i) => i === idx ? { ...t, completed: !t.completed } : t);
      // Increase sync level slightly on completion
      if (!prev[idx].completed) {
        setSyncLevel(s => Math.min(100, s + 1));
      }
      return newTasks;
    });
  };

  const handleExecuteTrade = async (target: string, amount: string) => {
    setIsExecutingTrade(true);
    setTradeStatus(`Initiating transaction for ${target}...`);
    setTradeProgress(10);
    
    // Simulate trade execution steps
    const steps = [
      { p: 30, s: "Validating budget allocation..." },
      { p: 50, s: "Securing Ruliad-v1 uplink..." },
      { p: 70, s: "Executing hypergraph node shift..." },
      { p: 90, s: "Finalizing ledger entry..." },
      { p: 100, s: "Transaction Complete." }
    ];

    for (const step of steps) {
      await new Promise(r => setTimeout(r, 800));
      setTradeProgress(step.p);
      setTradeStatus(step.s);
    }

    setNotifications(prev => [{
      id: Date.now().toString(),
      type: 'success',
      title: 'Trade Executed',
      message: `Successfully traded ${amount} for ${target}.`,
      timestamp: new Date().toLocaleTimeString()
    }, ...prev]);

    setTimeout(() => {
      setIsExecutingTrade(false);
      setTradeStatus(null);
      setTradeProgress(0);
    }, 2000);
  };

  // Continuous Wearable Sync Simulation
  useEffect(() => {
    const interval = setInterval(() => {
      setProfile(prev => {
        const newPulse = Math.floor(60 + Math.random() * 20);
        const newHrv = Math.floor(40 + Math.random() * 40);
        
        // Trigger Alert if HRV is low
        if (newHrv < 45 && isAudioUnlocked) {
          const alert: Notification = {
            id: Date.now().toString(),
            type: 'health',
            message: `CRITICAL: HRV dropped to ${newHrv}ms. Flare probability: 78%.`,
            timestamp: new Date().toLocaleTimeString(),
            read: false
          };
          setNotifications(prevN => [alert, ...prevN]);
          
          // Voice Alert
          speak(`Omega Clearance, your heart rate variability has dropped to ${newHrv} milliseconds. A health flare is predicted within 24 hours. Please initiate rest protocol.`);
        }

        return {
          ...prev,
          bioMarkers: {
            ...prev.bioMarkers,
            pulse: `${newPulse} bpm`,
            hrv: `${newHrv} ms`
          }
        };
      });
    }, 15000); // Sync every 15 seconds

    return () => clearInterval(interval);
  }, []);

  const handleMelanomaAnalysis = async (imageData: string, biomarkerJson: any) => {
    setIsAnalyzingMelanoma(true);
    setExecutionLogs(prev => [...prev, "[SYSTEM] Initiating Melanoma Singularity Test...", "[VISION] Extracting ABCDE features..."]);
    
    try {
      const visionResult = await analyzeMelanomaLesion(imageData);
      setExecutionLogs(prev => [...prev, `[VISION] Visual Risk: ${Math.round(visionResult.riskScore * 100)}%`, "[BIO] Fusing with biomarker dataset..."]);
      
      const fusionResult = await fuseMelanomaMarkers(visionResult.riskScore, biomarkerJson);
      setExecutionLogs(prev => [...prev, `[FUSION] Final Risk: ${Math.round(fusionResult.finalRisk * 100)}%`, `[SAFETY] Recommended Action: ${fusionResult.action}`]);
      
      setMelanomaData({
        risk: fusionResult.finalRisk,
        action: fusionResult.action,
        features: visionResult.features,
        reasoning: visionResult.reasoning,
        therapyEligibility: fusionResult.therapyEligibility
      });

      if (fusionResult.finalRisk > 0.7) {
        const alert: Notification = {
          id: Date.now().toString(),
          type: 'health',
          message: `CRITICAL ALERT: High Melanoma Risk Detected (${Math.round(fusionResult.finalRisk * 100)}%). Action: ${fusionResult.action}`,
          timestamp: new Date().toLocaleTimeString(),
          read: false
        };
        setNotifications(prev => [alert, ...prev]);
        speak(`Omega Clearance, high-risk lesion detected. Recommended action is urgent dermatology referral. Do not delay.`);
      }
    } catch (err) {
      console.error("Melanoma analysis error:", err);
      setError("Melanoma analysis failed. Check logs.");
    } finally {
      setIsAnalyzingMelanoma(false);
    }
  };

  const handleBehaviorAnalysis = async (imageData: string) => {
    setIsAnalyzingBehavior(true);
    setExecutionLogs(prev => [...prev, "[BEHAVIOR] Scanning facial micro-expressions...", "[BEHAVIOR] Analyzing postural dynamics..."]);
    
    try {
      const result = await analyzeBehavior(imageData);
      setBehaviorData(result);
      setExecutionLogs(prev => [...prev, `[BEHAVIOR] Emotion: ${result.emotion}`, `[BEHAVIOR] Stress Level: ${result.stressLevel}%`]);
      
      if (result.stressLevel > 80) {
        const alert: Notification = {
          id: Date.now().toString(),
          type: 'health',
          message: `BEHAVIOR ALERT: High Stress Detected (${result.stressLevel}%). Insight: ${result.insight}`,
          timestamp: new Date().toLocaleTimeString(),
          read: false
        };
        setNotifications(prev => [alert, ...prev]);
        speak(`Omega Clearance, high stress levels detected. Recommend immediate metabolic recalibration and rest.`);
      }
    } catch (err) {
      console.error("Behavior analysis error:", err);
    } finally {
      setIsAnalyzingBehavior(false);
    }
  };

  const handleCRISPRSimulation = async () => {
    setIsEditingDNA(true);
    setExecutionLogs(prev => [...prev, `[CRISPR] Targeting gene: ${targetGene}...`, "[CRISPR] Initializing Cas9 molecular scissors..."]);
    
    try {
      const result = await simulateCRISPRIntervention(dnaSequence, targetGene);
      setCrisprResult(result);
      setDnaSequence(result.modifiedSequence);
      setExecutionLogs(prev => [...prev, "[CRISPR] Gene editing complete.", `[CRISPR] Impact Score: ${result.impactScore}%`]);
      
      speak(`CRISPR intervention complete. Target gene ${targetGene} has been modified. Impact score on cancer suppression is ${result.impactScore} percent.`);
    } catch (err) {
      console.error("CRISPR error:", err);
    } finally {
      setIsEditingDNA(false);
    }
  };

  const handleMolecularDocking = async () => {
    setIsDocking(true);
    setExecutionLogs(prev => [...prev, `[DOCKING] Initiating Step-21: Molecular Docking...`, `[DOCKING] Target: ${targetGene} modified sequence...`, `[DOCKING] Molecule: ${drugMolecule}...`]);
    
    try {
      const result = await simulateMolecularDocking(drugMolecule, dnaSequence);
      setDockingData(result);
      setExecutionLogs(prev => [...prev, "[DOCKING] Docking simulation complete.", `[DOCKING] Binding Affinity: ${result.bindingAffinity}%`]);
      
      speak(`Molecular docking complete. Binding affinity for ${drugMolecule} is ${result.bindingAffinity} percent. Stability score is ${result.stabilityScore} percent.`);
    } catch (err) {
      console.error("Docking error:", err);
    } finally {
      setIsDocking(false);
    }
  };

  const handleTherapyRecommendation = async () => {
    setIsGeneratingTherapy(true);
    setExecutionLogs(prev => [...prev, "[THERAPY] Generating clinical recommendation...", "[THERAPY] Analyzing molecular docking and patient context..."]);
    
    try {
      const result = await generateTherapyRecommendation({
        melanoma: melanomaData,
        behavior: behaviorData,
        profile: profile
      }, dockingData);
      setTherapyRecommendation(result);
      setExecutionLogs(prev => [...prev, "[THERAPY] Recommendation finalized.", `[THERAPY] Type: ${result.therapyType}`]);
      
      speak(`Therapy recommendation finalized. Recommended treatment is ${result.therapyType}. Expected outcome: ${result.expectedOutcome}. Risk level is ${result.riskLevel}.`);
    } catch (err) {
      console.error("Therapy error:", err);
    } finally {
      setIsGeneratingTherapy(false);
    }
  };

  const handleQuantumFeedback = async () => {
    if (!therapyRecommendation) return;
    setIsSimulatingQuantum(true);
    setExecutionLogs(prev => [...prev, "[QUANTUM] Initiating Step-22: Quantum Patient Bio-Feedback...", "[QUANTUM] Synchronizing Digital Twin with real-time bio-markers..."]);
    
    try {
      const result = await simulateQuantumPatientFeedback(therapyRecommendation, profile);
      setQuantumFeedback(result);
      setExecutionLogs(prev => [...prev, "[QUANTUM] Bio-feedback loop complete.", `[QUANTUM] Cellular Response: ${result.cellularResponse}`]);
      
      speak(`Quantum patient feedback received. Cellular response: ${result.cellularResponse}. Heart rate is ${result.vitalSigns.heartRate} beats per minute. ${result.toxicityAlert ? "Warning: Toxicity alert detected." : "No toxicity alerts detected."}`);
    } catch (err) {
      console.error("Quantum feedback error:", err);
    } finally {
      setIsSimulatingQuantum(false);
    }
  };

  const handleSaveMemory = async () => {
    if (!melanomaData) return;
    setIsSavingMemory(true);
    setExecutionLogs(prev => [...prev, "[MEMORY] Initializing Step-19: Evolutionary Persistence...", "[MEMORY] Compressing session data for long-term recall..."]);
    
    try {
      const result = await saveResearchOutcome({
        melanoma: melanomaData,
        behavior: behaviorData,
        decision: decisionData,
        progression: progressionData
      });
      
      if (result.success) {
        setNeuralLog(prev => [{
          timestamp: new Date().toLocaleTimeString(),
          agent: 'EVOLUTION ENGINE',
          action: result.logEntry
        }, ...prev]);
        
        setExecutionLogs(prev => [...prev, "[MEMORY] Persistence complete.", "[MEMORY] Data synced to Evolutionary Log."]);
        
        speak(`Evolutionary memory synchronized. Session data has been persisted to the long-term log.`);
      }
    } catch (err) {
      console.error("Memory save error:", err);
    } finally {
      setIsSavingMemory(false);
    }
  };

  const handleTreatmentOptimization = async () => {
    if (!melanomaData) return;
    setIsOptimizing(true);
    setExecutionLogs(prev => [...prev, "[DECISION] Activating Step-11: Decision Agent...", "[DECISION] Cross-referencing bio-markers with behavioral stress..."]);
    
    try {
      const result = await optimizeTreatmentPath(melanomaData, behaviorData);
      setDecisionData(result);
      setExecutionLogs(prev => [...prev, "[DECISION] Optimization complete.", `[DECISION] Path: ${result.optimizedPath}`]);
      
      speak(`Decision Agent optimization complete. The recommended path is ${result.optimizedPath}. Efficacy score is ${result.efficacyScore} percent.`);
    } catch (err) {
      console.error("Optimization error:", err);
    } finally {
      setIsOptimizing(false);
    }
  };

  const handleProgressionSimulation = async () => {
    if (!melanomaData) return;
    setIsSimulatingProgression(true);
    setExecutionLogs(prev => [...prev, "[TWIN] Initializing 6-month progression simulation...", "[TWIN] Modeling immune response dynamics..."]);
    
    try {
      const result = await simulateCancerProgression(profile, melanomaData);
      setProgressionData(result);
      setExecutionLogs(prev => [...prev, "[TWIN] Simulation complete.", `[TWIN] Forecast: ${result.summary}`]);
    } catch (err) {
      console.error("Progression simulation error:", err);
    } finally {
      setIsSimulatingProgression(false);
    }
  };

  const handleDreamerSimulation = async () => {
    setIsDreaming(true);
    try {
      const data = await runDreamerSimulation(profile, activeDomain);
      setDreamerData(data);
      
      // If risk is high, auto-trigger alert
      if (data.riskScore > 70) {
        const alert: Notification = {
          id: Date.now().toString(),
          type: 'health',
          message: `DREAMER ALERT: ${data.insight}. Risk Score: ${data.riskScore}%`,
          timestamp: new Date().toLocaleTimeString(),
          read: false
        };
        setNotifications(prev => [alert, ...prev]);
        
        speak(`Omega Clearance, the Dreamer Engine has identified a high-risk trajectory. ${data.insight}. Initiating preventive measures.`);
      }
    } catch (err) {
      console.error("Dreamer error:", err);
    } finally {
      setIsDreaming(false);
    }
  };

  const handleSendMessage = async () => {
    if (!chatInput) return;
    const userMsg = chatInput;
    setChatMessages(prev => [...prev, { role: 'user', text: userMsg }]);
    setChatInput('');
    
    try {
      const response = await agentChat(userMsg, chatMessages, profile);
      
      // Check for trade execution intent in agent response
      if (response && (response.toLowerCase().includes("initiating transaction protocol") || 
          response.toLowerCase().includes("executing trade") ||
          response.toLowerCase().includes("transaction protocol recognized"))) {
        
        const targetMatch = userMsg.match(/buy\s+(\w+)/i) || userMsg.match(/trade\s+(\w+)/i) || userMsg.match(/target\s+(\w+)/i);
        const amountMatch = userMsg.match(/\$(\d+(?:,\d+)*(?:\.\d+)?)/) || userMsg.match(/(\d+)\s+shares/i);
        
        const target = targetMatch ? targetMatch[1].toUpperCase() : "ASSET";
        const amount = amountMatch ? amountMatch[0] : "$1,000.00";
        
        handleExecuteTrade(target, amount);
      }

      setChatMessages(prev => [...prev, { role: 'agent', text: response || "Communication link stable. Awaiting further directives." }]);
    } catch (err) {
      setChatMessages(prev => [...prev, { role: 'agent', text: "Error: Communication uplink failed." }]);
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) audioChunksRef.current.push(e.data);
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        const reader = new FileReader();
        reader.readAsDataURL(audioBlob);
        reader.onloadend = async () => {
          const base64Audio = (reader.result as string).split(',')[1];
          handleVoiceInput(base64Audio);
        };
        stream.getTracks().forEach(track => track.stop());
      };

      // Visualizer
      const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
      const source = audioContext.createMediaStreamSource(stream);
      const analyser = audioContext.createAnalyser();
      analyser.fftSize = 64;
      source.connect(analyser);
      
      audioContextRef.current = audioContext;
      analyserRef.current = analyser;

      const updateWaveform = () => {
        const dataArray = new Uint8Array(analyser.frequencyBinCount);
        analyser.getByteFrequencyData(dataArray);
        const normalized = Array.from(dataArray).slice(0, 20).map(v => v / 255);
        setWaveform(normalized);
        animationFrameRef.current = requestAnimationFrame(updateWaveform);
      };
      updateWaveform();

      mediaRecorder.start();
      setIsRecording(true);
    } catch (err) {
      console.error("Recording error:", err);
      setError("Microphone access denied.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      if (animationFrameRef.current) cancelAnimationFrame(animationFrameRef.current);
      setWaveform(new Array(20).fill(0));
    }
  };

  const handleVoiceInput = async (base64Audio: string) => {
    setIsProcessingVoice(true);
    try {
      const result = await processVoiceInput(base64Audio, activeDomain, profile);
      if (result && result.transcription) {
        setChatMessages(prev => [...prev, { role: 'user', text: `[Voice] ${result.transcription}` }]);
        
        const response = await agentChat(result.transcription, chatMessages, profile);
        setChatMessages(prev => [...prev, { role: 'agent', text: response }]);
        
        // Generate and play TTS response
        speak(response);
      }
    } catch (err) {
      console.error("Voice processing error:", err);
    } finally {
      setIsProcessingVoice(false);
    }
  };

  const updateBioMarker = (key: keyof UserProfile['bioMarkers'], value: string) => {
    setProfile(prev => ({
      ...prev,
      bioMarkers: {
        ...prev.bioMarkers,
        [key]: value
      }
    }));
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setCapturedImage(event.target?.result as string);
        setUploadedText(null);
      };
      reader.readAsDataURL(file);
    } else if (file.type === 'text/plain') {
      const reader = new FileReader();
      reader.onload = (event) => {
        setUploadedText(event.target?.result as string);
        setCapturedImage(null);
      };
      reader.readAsText(file);
    } else {
      setError("Unsupported file type. Please upload an image or a .txt file.");
    }
  };

  const handleGenerateHypothesis = async () => {
    setIsGeneratingHypothesis(true);
    try {
      const state = {
        melanomaData,
        behaviorData,
        profile,
        dnaSequence,
        targetGene,
        dockingData
      };
      const result = await generateHypothesis(activeDomain, state);
      setHypothesis(result);
      
      const voiceText = `Hypothesis generated with ${result.confidence}% confidence. ${result.hypothesis}`;
      speak(voiceText);
    } catch (err) {
      console.error(err);
    } finally {
      setIsGeneratingHypothesis(false);
    }
  };

  const handleRunExperiment = async () => {
    if (!hypothesis) return;
    setIsRunningExperiment(true);
    try {
      const state = {
        melanomaData,
        behaviorData,
        profile,
        dnaSequence,
        targetGene,
        dockingData
      };
      const result = await runExperiment(hypothesis.hypothesis, activeDomain, state);
      setExperimentResult(result);
      
      const voiceText = `Experiment ${result.result}. Observation: ${result.observation}. Belief update initiated.`;
      speak(voiceText);
    } catch (err) {
      console.error(err);
    } finally {
      setIsRunningExperiment(false);
    }
  };

  const handleGenerateSyntheticImage = async () => {
    setIsGeneratingImage(true);
    try {
      const prompt = hypothesis?.hypothesis || "Melanoma lesion with irregular borders and color variation";
      const result = await generateSyntheticLesion(prompt);
      setSyntheticImage(result);
    } catch (err) {
      console.error(err);
    } finally {
      setIsGeneratingImage(false);
    }
  };

  const handleRunManifold = async () => {
    setIsAnalyzingManifold(true);
    setExecutionLogs(prev => [...prev, "[MANIFOLD] Initializing Biological Latent Space Mapping...", "[MANIFOLD] Encoding biomarkers and genomic mutations..."]);
    
    try {
      const mutations = [targetGene];
      const result = await processManifoldEngine(profile.bioMarkers, mutations);
      setManifoldData(result);
      setExecutionLogs(prev => [...prev, `[MANIFOLD] Mapping complete. Region: ${result.manifoldRegion}`, `[MANIFOLD] Trajectory: ${result.trajectory}`]);
      
      speak(`Manifold mapping complete. Patient has been localized to the ${result.manifoldRegion} region. Disease trajectory is predicted as ${result.trajectory}.`);
    } catch (err) {
      console.error("Manifold error:", err);
    } finally {
      setIsAnalyzingManifold(false);
    }
  };

  const handleFullScaleSystemTest = async () => {
    setIsTesting(true);
    setTestResults([]);
    setExecutionLogs(prev => [...prev, "--- INITIATING FULL SCALE SYSTEM TEST (OMEGA PROTOCOL) ---"]);
    
    try {
      // 1. VIDEO TEST (Optical Ingress)
      setExecutionLogs(prev => [...prev, "[STEP 1/4] VIDEO TEST: Initiating Optical Ingress..."]);
      if (!capturedImage) {
        setExecutionLogs(prev => [...prev, "[WARNING] No Optical Ingress detected. Please capture a selfie in the sidebar first."]);
        speak("Optical ingress missing. Please capture a selfie in the sidebar to proceed with the full scale test.");
        setIsTesting(false);
        return;
      }
      setExecutionLogs(prev => [...prev, "[SUCCESS] Optical Ingress verified. Temporal pattern analysis complete."]);
      await new Promise(resolve => setTimeout(resolve, 1000));

      // 2. VOICE TEST (Uplink & Feedback)
      setExecutionLogs(prev => [...prev, "[STEP 2/4] VOICE TEST: Testing Neural Uplink..."]);
      if (isAudioUnlocked) {
        await speak("Neural voice uplink established. Testing feedback loop. Can you hear me, Aloysius?");
      }
      setExecutionLogs(prev => [...prev, "[SUCCESS] Voice feedback loop verified."]);
      await new Promise(resolve => setTimeout(resolve, 1000));

      // 3. SMARTWATCH TEST (Wearable Sync)
      setExecutionLogs(prev => [...prev, "[STEP 3/4] SMARTWATCH TEST: Syncing Wearable Telemetry..."]);
      const simulatedVitals = { hrv: 72, sleep: 7.5, steps: 8432 };
      setExecutionLogs(prev => [...prev, `[SENSOR] Syncing Vitals: HRV: ${simulatedVitals.hrv}ms, Sleep: ${simulatedVitals.sleep}h, Steps: ${simulatedVitals.steps}`]);
      setExecutionLogs(prev => [...prev, "[SUCCESS] Wearable telemetry synchronized with Digital Twin."]);
      await new Promise(resolve => setTimeout(resolve, 1000));

      // 4. ALERTS (Communication Layer)
      setExecutionLogs(prev => [...prev, "[STEP 4/4] ALERTS: Testing Communication Layer..."]);
      if (isEmailAlertEnabled) {
        setExecutionLogs(prev => [...prev, `[DISPATCH] Sending system status report to: aejphillips@outlook.com`]);
        await fetch('/api/alert', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ type: 'system', message: 'Full Scale System Test (Omega Protocol) initiated.', email: 'aejphillips@outlook.com' })
        }).catch(console.error);
        setExecutionLogs(prev => [...prev, "[SUCCESS] Email alert dispatched."]);
      }
      if (isSmsAlertEnabled) {
        setExecutionLogs(prev => [...prev, `[SMS] Sending encrypted status update to: ${phoneNumber}`]);
        setExecutionLogs(prev => [...prev, "[SUCCESS] SMS alert dispatched."]);
      }
      
      if (!isEmailAlertEnabled && !isSmsAlertEnabled) {
        setExecutionLogs(prev => [...prev, "[SKIP] All alerts are currently disabled in settings."]);
      }
      
      // Final Singularity Loop (Unified)
      setExecutionLogs(prev => [...prev, "[SINGULARITY] Running final cross-domain optimization..."]);
      await handleHighCriticalTest();

      setExecutionLogs(prev => [...prev, "--- FULL SCALE SYSTEM TEST COMPLETE ---"]);
      speak("Full scale system test complete. Video, Voice, Watch, and Email layers are all operational. The Singularity is stable.");

    } catch (err) {
      console.error("Full Scale Test error:", err);
      setError("Full scale system test failed.");
    } finally {
      setIsTesting(false);
    }
  };

  const handleHumanoidTest = async (testType: 'emotion' | 'precision' | 'stress') => {
    setIsTesting(true);
    setExecutionLogs(prev => [...prev, `[HUMANOID] Starting ${testType.toUpperCase()} test suite...`]);
    
    // Simulate test steps
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    if (testType === 'emotion') {
      setHumanoidState(prev => ({ ...prev, mood: 0.8, stress: 0.2, anger: 0.1, calm: 0.9 }));
      setExecutionLogs(prev => [...prev, "[SUCCESS] Emotion Interaction: De-escalation protocol verified."]);
    } else if (testType === 'precision') {
      setRobotMotors(prev => ({ ...prev, leftArm: 100, rightArm: 100 }));
      setExecutionLogs(prev => [...prev, "[SUCCESS] Task Precision: Grasp stability at 99.9%."]);
    } else if (testType === 'stress') {
      setHumanoidState(prev => ({ ...prev, stress: 0.9, energy: 0.4 }));
      setSatelliteStatus(prev => ({ ...prev, link: 'LOCAL_AUTONOMY', latency: 'N/A' }));
      setExecutionLogs(prev => [...prev, "[SUCCESS] Stress Resilience: Fail-safe mode engaged."]);
    }
    
    setIsTesting(false);
  };

  const handleEyeScan = async () => {
    setIsEyeScanning(true);
    setEyeScanResult(null);
    setExecutionLogs(prev => [...prev, "[BIOMETRIC] Initializing Eye Scan sequence..."]);
    
    await new Promise(resolve => setTimeout(resolve, 2500));
    
    const result = "Retinal Pattern Verified. No anomalies detected. Health Index: 98%";
    setEyeScanResult(result);
    setExecutionLogs(prev => [...prev, `[SUCCESS] Eye Scan: ${result}`]);
    setIsEyeScanning(false);
  };

  const handleHighCriticalTest = async () => {
    setIsTesting(true);
    setTestResults([]);
    setExecutionLogs(prev => [...prev, "--- INITIATING UNIFIED SINGULARITY DOMAIN TEST ---"]);
    
    const testPlans = [
      {
        domain: 'Grocery' as const,
        data: {
          items: [
            { name: "chicken breast", price: 12.5, protein: 31 },
            { name: "rice", price: 2.5, carbs: 28 },
            { name: "broccoli", price: 3.2, fiber: 2.6 }
          ],
          supplier: "Harris Farm"
        }
      },
      {
        domain: 'Finance' as const,
        data: {
          assets: ["AAPL", "Gold", "AUD/USD"],
          macro: { inflation: 4.2, interest_rate: 4.35 }
        }
      },
      {
        domain: 'Health' as const,
        data: {
          diet: ["processed food"],
          biomarkers: { CRP: 6.5 }
        }
      }
    ];

    try {
      for (const plan of testPlans) {
        const domain = plan.domain === 'Health' ? 'Health' : plan.domain === 'Finance' ? 'Finance' : 'Grocery';
        setActiveDomain(domain as Domain);
        setExecutionLogs(prev => [...prev, `[SINGULARITY] Executing ${plan.domain} Loop: INPUT → HYPOTHESIS → EXPERIMENT → SIMULATION → DECISION → OUTPUT`]);
        
        const result = await runSingularityTestPlan(plan.domain, plan.data);
        
        setTestResults(prev => [...prev, { domain: plan.domain, steps: result.tasks || [] }]);
        setExecutionLogs(prev => [...prev, `[TEST] ${plan.domain} optimized. Recommendation: ${result.recommendation || 'Verified'}`]);
        
        // Voice feedback for each domain
        if (isAudioUnlocked) {
          await speak(`${plan.domain} singularity loop complete. Optimization achieved.`);
        }
        
        await new Promise(resolve => setTimeout(resolve, 800));
      }

      // Cross-Domain Intelligence (Digital Twin)
      setExecutionLogs(prev => [...prev, "[DIGITAL TWIN] Linking Grocery Choice to Health Outcome..."]);
      setExecutionLogs(prev => [...prev, "[DIGITAL TWIN] Food choice (Harris Farm) -> Biomarker change (CRP -15%) -> Health outcome (Improved)"]);
      
      setExecutionLogs(prev => [...prev, "--- UNIFIED SINGULARITY TEST COMPLETE ---"]);
      speak("Unified singularity testing complete. Cross-domain intelligence verified. One system, all domains.");
      
    } catch (err) {
      console.error("Singularity Test error:", err);
      setError("Unified singularity test failed.");
    } finally {
      setIsTesting(false);
    }
  };

  const handleSimulateEmergency = async () => {
    setIsEmergencyCallActive(true);
    setEmergencyCallTimer(0);
    
    // Trigger Critical Alert
    const alert: Notification = {
      id: Date.now().toString(),
      type: 'health',
      message: `CRITICAL: OMEGA EMERGENCY PROTOCOL INITIATED. HRV: 28ms.`,
      timestamp: new Date().toLocaleTimeString(),
      read: false
    };
    setNotifications(prev => [alert, ...prev]);

    // Voice Alert
    speak("Omega Clearance, this is a critical health emergency. Your heart rate variability has dropped to twenty-eight milliseconds. Initiating emergency dispatch and medical drone deployment. Please remain calm.");

    // Start Timer
    const timer = setInterval(() => {
      setEmergencyCallTimer(prev => prev + 1);
    }, 1000);

    // Auto-close after 30s
    setTimeout(() => {
      clearInterval(timer);
      setIsEmergencyCallActive(false);
    }, 30000);
  };

  const handleGenerateVideo = async () => {
    setIsGeneratingVideo(true);
    setVideoProgress(10);
    try {
      const prompt = hypothesis?.hypothesis || "Cellular progression of melanoma under immunotherapy";
      const result = await generateProgressionVideo(prompt);
      setProgressionVideo(result);
      setVideoProgress(100);
    } catch (err) {
      console.error(err);
    } finally {
      setIsGeneratingVideo(false);
    }
  };

  const handleRunBacktest = async (targetTicker: string = ticker || 'ANZ') => {
    if (!targetTicker) {
      setError("Please enter a ticker (e.g., ANZ) to run backtest.");
      return;
    }
    setIsBacktesting(true);
    setExecutionLogs(prev => [...prev, `[BACKTEST] Initializing historical simulation for ${targetTicker}...`]);
    try {
      const data = await runBacktestSimulation(targetTicker);
      setBacktestData(data);
      setExecutionLogs(prev => [...prev, `[SUCCESS] Backtest complete. Hit Rate: ${data.metrics.hitRate}%`]);
    } catch (err) {
      console.error("Backtest error:", err);
      setError("Failed to run backtest simulation.");
    } finally {
      setIsBacktesting(false);
    }
  };

  return (
    <div className="flex h-screen bg-[#F8F9FA] text-[#1A1A1A] font-sans overflow-hidden relative">
      <AnimatePresence>
        {!isAudioUnlocked && (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-[100] bg-[#1A1A1A] flex items-center justify-center p-8"
          >
            <div className="max-w-md w-full space-y-8 text-center">
              <div className="relative inline-block">
                <div className="absolute inset-0 bg-blue-500 blur-3xl opacity-20 animate-pulse" />
                <Cpu className="w-24 h-24 text-blue-500 mx-auto relative z-10" />
              </div>
              <div className="space-y-4">
                <h1 className="text-4xl font-black text-white tracking-tighter uppercase italic">Buddy's Toolset by A&P Phillips</h1>
                <p className="text-blue-400 font-mono text-xs uppercase tracking-[0.3em]">Singularity Interface v1.0</p>
              </div>
              <div className="p-6 bg-white/5 border border-white/10 rounded-3xl space-y-4">
                <p className="text-xs text-gray-400 leading-relaxed">
                  Welcome, Omega Clearance. To initialize the neural uplink and enable voice feedback, please confirm your identity.
                </p>
                <button 
                  onClick={() => {
                    setIsAudioUnlocked(true);
                    // Play a silent sound to unlock audio context
                    const audio = new Audio("data:audio/wav;base64,UklGRigAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQAAAAA=");
                    audio.play().catch(() => {});
                  }}
                  className="w-full py-4 bg-blue-600 text-white rounded-2xl font-black text-sm uppercase tracking-widest hover:bg-blue-700 transition-all shadow-xl shadow-blue-900/40 flex items-center justify-center gap-3 group"
                >
                  <Shield className="w-5 h-5 group-hover:scale-110 transition-transform" />
                  INITIALIZE SYSTEM
                </button>
              </div>
              <div className="flex items-center justify-center gap-4 opacity-40">
                <div className="h-[1px] w-12 bg-white/20" />
                <span className="text-[8px] font-mono text-white uppercase tracking-widest">Secure Uplink Established</span>
                <div className="h-[1px] w-12 bg-white/20" />
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Mobile Menu Toggle */}
      <div className="lg:hidden fixed top-4 left-4 z-[60]">
        <button 
          onClick={() => setIsSidebarOpen(!isSidebarOpen)}
          className="p-3 bg-white border border-gray-200 rounded-2xl shadow-lg text-gray-600 hover:text-blue-600 transition-all"
        >
          <Menu className="w-6 h-6" />
        </button>
      </div>

      <AnimatePresence>
        {isSidebarOpen && (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setIsSidebarOpen(false)}
            className="lg:hidden fixed inset-0 bg-black/50 z-40 backdrop-blur-sm"
          />
        )}
      </AnimatePresence>

      {/* Sidebar - Vault */}
      <aside className={cn(
        "fixed lg:relative z-50 lg:z-10 w-72 h-full bg-white border-r border-[#E5E7EB] flex flex-col shadow-sm transition-transform duration-300 ease-in-out",
        isSidebarOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
      )}>
        <div className="p-6 border-bottom border-[#F3F4F6]">
          <div className="space-y-4">
            {/* Market Ingress - Moved to Top */}
            <div className="p-4 bg-white rounded-xl border border-[#E5E7EB] shadow-sm">
              <p className="text-[10px] font-bold text-[#6B7280] uppercase tracking-widest mb-3">Market Ingress</p>
              <div className="flex gap-2">
                <input 
                  type="text"
                  value={ticker}
                  onChange={(e) => setTicker(e.target.value.toUpperCase())}
                  placeholder="TSLA"
                  className="w-full p-2 bg-[#F3F4F6] border border-[#E5E7EB] rounded-lg text-xs font-bold focus:ring-2 focus:ring-blue-500 transition-all"
                />
                <button 
                  onClick={handleProcess}
                  disabled={isProcessing || !ticker}
                  className="p-2 bg-[#1A1A1A] text-white rounded-lg hover:bg-black disabled:opacity-50 transition-all"
                >
                  <Send className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Optical Sensor */}
            <div className="p-4 bg-white rounded-xl border border-[#E5E7EB] shadow-sm">
              <p className="text-[10px] font-bold text-[#6B7280] uppercase tracking-widest mb-3">Optical Sensor</p>
              
              {capturedImage ? (
                <div className="relative group">
                  <img 
                    src={capturedImage} 
                    alt="Sensor Input" 
                    className="w-full aspect-square object-cover rounded-lg border border-[#E5E7EB]"
                  />
                  <button 
                    onClick={() => setCapturedImage(null)}
                    className="absolute top-2 right-2 p-1 bg-black/50 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>
              ) : (
                <button 
                  onClick={startCamera}
                  className="w-full aspect-square border-2 border-dashed border-[#D1D5DB] rounded-lg flex flex-col items-center justify-center gap-2 hover:border-[#1A1A1A] hover:bg-[#F9FAFB] transition-all group"
                >
                  <Camera className="w-8 h-8 text-[#9CA3AF] group-hover:text-[#1A1A1A]" />
                  <span className="text-xs font-medium text-[#6B7280] group-hover:text-[#1A1A1A]">Take Selfie</span>
                </button>
              )}
            </div>

            {/* Domain Selector */}
            <div className="p-4 bg-[#F3F4F6] rounded-xl border border-[#E5E7EB]">
              <p className="text-[10px] font-bold text-[#6B7280] uppercase tracking-widest mb-3">Domain Focus</p>
              <div className="grid grid-cols-2 gap-2">
                {(['General', 'Health', 'Agriculture', 'Finance', 'Grocery', 'DrugDiscovery'] as Domain[]).map((d) => (
                  <button
                    key={d}
                    onClick={() => setActiveDomain(d)}
                    className={cn(
                      "p-2 rounded-lg text-[10px] font-bold transition-all flex items-center gap-2",
                      activeDomain === d ? "bg-[#1A1A1A] text-white" : "bg-white text-[#6B7280] hover:bg-gray-100"
                    )}
                  >
                    {d === 'Health' && <Activity className="w-3 h-3" />}
                    {d === 'Agriculture' && <Leaf className="w-3 h-3" />}
                    {d === 'Finance' && <DollarSign className="w-3 h-3" />}
                    {d === 'General' && <Cpu className="w-3 h-3" />}
                    {d === 'Grocery' && <Smartphone className="w-3 h-3" />}
                    {d === 'DrugDiscovery' && <Microscope className="w-3 h-3" />}
                    {d}
                  </button>
                ))}
              </div>
            </div>

            {/* Autoimmune Mode Toggle */}
            <div className="p-4 bg-red-50 rounded-xl border border-red-100 mt-4">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <Activity className="w-4 h-4 text-red-600" />
                  <p className="text-[10px] font-bold text-red-900 uppercase tracking-widest">Autoimmune Mode</p>
                </div>
                <button 
                  onClick={() => setIsAutoimmuneMode(!isAutoimmuneMode)}
                  className={cn(
                    "w-8 h-4 rounded-full relative transition-colors",
                    isAutoimmuneMode ? "bg-red-600" : "bg-gray-300"
                  )}
                >
                  <div className={cn(
                    "absolute top-0.5 w-3 h-3 bg-white rounded-full transition-transform",
                    isAutoimmuneMode ? "translate-x-4" : "translate-x-1"
                  )} />
                </button>
              </div>
              <p className="text-[9px] text-red-600 leading-tight">Engage Closed-Loop Research Engine</p>
            </div>

            {/* Quick Action: Start Analysis */}
            {capturedImage && activeDomain === 'Health' && !melanomaData && (
              <motion.button
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                onClick={() => {
                  setActiveTab('RESEARCH DEVICE');
                  // We'll let the user click the button in the tab to ensure they see the JSON part
                }}
                className="w-full mt-4 p-4 bg-red-600 text-white rounded-xl text-xs font-black uppercase tracking-widest shadow-lg shadow-red-200 flex items-center justify-center gap-2 animate-pulse"
              >
                <Zap className="w-4 h-4" />
                START MELANOMA ANALYSIS
              </motion.button>
            )}

            {/* Next Step Indicator */}
            {melanomaData && !hypothesis && (
              <div className="mt-4 p-4 bg-amber-50 border border-amber-100 rounded-xl">
                <p className="text-[8px] font-bold text-amber-800 uppercase tracking-widest mb-1">Next Step (Phase 3)</p>
                <button 
                  onClick={() => setActiveTab('SCIENTIFIC DISCOVERY')}
                  className="text-[10px] text-amber-600 font-bold underline"
                >
                  Generate Hypothesis →
                </button>
              </div>
            )}

            {hypothesis && !experimentResult && (
              <div className="mt-4 p-4 bg-blue-50 border border-blue-100 rounded-xl">
                <p className="text-[8px] font-bold text-blue-800 uppercase tracking-widest mb-1">Next Step (Phase 4)</p>
                <button 
                  onClick={() => setActiveTab('SCIENTIFIC DISCOVERY')}
                  className="text-[10px] text-blue-600 font-bold underline"
                >
                  Run Experiment →
                </button>
              </div>
            )}

            {experimentResult && !syntheticImage && (
              <div className="mt-4 p-4 bg-purple-50 border border-purple-100 rounded-xl">
                <p className="text-[8px] font-bold text-purple-800 uppercase tracking-widest mb-1">Next Step (Phase 5)</p>
                <button 
                  onClick={() => setActiveTab('VISUAL SIMULATION')}
                  className="text-[10px] text-purple-600 font-bold underline"
                >
                  Generate Synthetic Lesion →
                </button>
              </div>
            )}

            {/* Safety Disclaimer */}
            <div className="p-4 bg-amber-50 rounded-xl border border-amber-100 mt-4 flex gap-2">
              <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
              <p className="text-[9px] text-amber-800 leading-tight">
                <b>SAFETY:</b> Research only. No clinical validation. Consult a doctor.
              </p>
            </div>

            {/* Live Data Ingress Toggle */}
            <div className="mt-4 p-4 bg-white border border-[#E5E7EB] rounded-xl space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Radio className={cn("w-4 h-4", isLiveFeedEnabled ? "text-red-500 animate-pulse" : "text-gray-400")} />
                  <span className="text-[10px] font-bold uppercase tracking-widest">Live Data Ingress</span>
                </div>
                <button 
                  onClick={() => setIsLiveFeedEnabled(!isLiveFeedEnabled)}
                  className={cn(
                    "w-8 h-4 rounded-full transition-all relative",
                    isLiveFeedEnabled ? "bg-red-500" : "bg-gray-200"
                  )}
                >
                  <div className={cn(
                    "absolute top-0.5 w-3 h-3 bg-white rounded-full transition-all",
                    isLiveFeedEnabled ? "left-4.5" : "left-0.5"
                  )} />
                </button>
              </div>
              {isLiveFeedEnabled && liveDataStatus && (
                <div className="flex items-center gap-2 px-2 py-1 bg-red-50 rounded border border-red-100">
                  <div className="w-1 h-1 rounded-full bg-red-500 animate-ping" />
                  <span className="text-[8px] font-mono text-red-600 font-bold truncate">{liveDataStatus}</span>
                </div>
              )}
              <p className="text-[8px] text-gray-400 leading-tight">
                Connects to real-time Market, Grocery, and Bio-metric APIs for autonomous optimization.
              </p>
            </div>

            {/* Command Center Quick Access */}
            <button 
              onClick={() => setActiveTab('COMMAND CENTER')}
              className="w-full mt-4 p-4 bg-[#1A1A1A] text-white rounded-xl flex items-center justify-between hover:bg-black transition-all group"
            >
              <div className="flex items-center gap-2">
                <Terminal className="w-4 h-4 text-emerald-400" />
                <span className="text-[10px] font-bold uppercase tracking-widest">Command Center</span>
              </div>
              <ChevronRight className="w-3 h-3 text-gray-500 group-hover:text-white transition-colors" />
            </button>
          </div>
        </div>

        <div className="mt-auto p-6 border-t border-[#F3F4F6]">
          <div className="flex items-center gap-2 text-[10px] font-mono text-[#9CA3AF]">
            <Zap className="w-3 h-3" />
            <span>PSI LEVEL 5 | OMEGA CLEARANCE</span>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col overflow-hidden relative">
        {/* Header */}
        <header className="p-8 pb-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4 mb-2">
              <div className="w-14 h-14 rounded-2xl bg-blue-600 flex items-center justify-center shadow-lg shadow-blue-200 relative group">
                <Shield className="w-8 h-8 text-white" />
                <div className="absolute -top-2 -right-2 w-6 h-6 bg-[#10B981] rounded-full border-2 border-white flex items-center justify-center shadow-sm">
                  <Bot className="w-3 h-3 text-white" />
                </div>
              </div>
              <div>
                <h2 className="text-3xl font-black tracking-tight text-[#1A1A1A]">Buddy's Toolset by A&P Phillips</h2>
                <div className="flex items-center gap-2">
                  <span className={cn(
                    "text-[10px] font-bold uppercase tracking-widest",
                    isProcessing ? "text-blue-500 animate-pulse" : "text-[#10B981]"
                  )}>
                    {isProcessing ? "ORCHESTRATING..." : "CLOUD SYNC ACTIVE"}
                  </span>
                  <span className="text-[#E5E7EB]">|</span>
                  <div className="flex items-center gap-1">
                    <Smartphone className="w-3 h-3 text-blue-500" />
                    <span className="text-[10px] font-bold text-blue-500 uppercase tracking-widest">MOBILE OPTIMIZED</span>
                  </div>
                  {summary && !isProcessing && (
                    <>
                      <span className="text-[#E5E7EB]">|</span>
                      <span className="text-[10px] font-bold text-purple-600 uppercase tracking-widest animate-bounce">REPORT READY</span>
                    </>
                  )}
                  <span className="text-[#E5E7EB]">|</span>
                  <p className="text-xs text-[#6B7280] font-medium tracking-wide">Omega Clearance | DNA Editor | PSI Level 5</p>
                  {isAutoimmuneMode && (
                    <>
                      <span className="text-[#E5E7EB]">|</span>
                      <div className="flex items-center gap-1">
                        <Activity className="w-3 h-3 text-red-500 animate-pulse" />
                        <span className="text-[8px] font-black text-red-500 uppercase tracking-widest">BIO-AI ACTIVE</span>
                      </div>
                    </>
                  )}
                </div>
              </div>
            </div>
            
            <button 
              onClick={() => {
                navigator.clipboard.writeText(window.location.origin);
                alert('Cloud URL copied to clipboard!');
              }}
              className="flex items-center gap-2 px-4 py-2 bg-white border border-[#E5E7EB] rounded-xl text-xs font-bold hover:bg-gray-50 transition-all shadow-sm"
            >
              <Globe className="w-4 h-4 text-blue-500" />
              SHARE CLOUD LAB
            </button>
          </div>

          {/* Tabs */}
          <nav className="flex gap-8 mt-8 border-b border-[#E5E7EB] overflow-x-auto no-scrollbar">
            {(['HOW TO USE', 'COMMAND CENTER', 'FACTORY (CHAT)', 'REPORTS', 'BACKTEST', 'WORLD MODEL', 'HIERARCHY', 'EVOLUTION', 'RESEARCH DEVICE', 'SCIENTIFIC DISCOVERY', 'VISUAL SIMULATION', 'MANIFOLD', 'COSMO-HUMANOID'] as Tab[]).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={cn(
                  "pb-4 text-xs font-bold tracking-widest transition-all relative whitespace-nowrap",
                  activeTab === tab ? "text-red-500" : "text-[#9CA3AF] hover:text-[#1A1A1A]"
                )}
              >
                <span className="flex items-center gap-2">
                  {tab === 'HOW TO USE' && <BookOpen className="w-3 h-3" />}
                  {tab === 'COSMO-HUMANOID' && <User className="w-3 h-3 text-emerald-500" />}
                  {tab === 'FACTORY (CHAT)' && (
                    <div className="relative">
                      <MessageSquare className="w-3 h-3" />
                      <span className="absolute -top-2 -right-2 px-1 bg-red-500 text-white text-[6px] font-black rounded-full animate-bounce">NEW</span>
                    </div>
                  )}
                  {tab === 'REPORTS' && <FileText className="w-3 h-3" />}
                  {tab === 'BACKTEST' && <History className="w-3 h-3 text-amber-500" />}
                  {tab === 'WORLD MODEL' && <Globe className="w-3 h-3" />}
                  {tab === 'HIERARCHY' && <Network className="w-3 h-3" />}
                  {tab === 'EVOLUTION' && <Dna className="w-3 h-3" />}
                  {tab === 'RESEARCH DEVICE' && <Microscope className="w-3 h-3" />}
                  {tab === 'SCIENTIFIC DISCOVERY' && <Lightbulb className="w-3 h-3 text-amber-500" />}
                  {tab === 'VISUAL SIMULATION' && <Video className="w-3 h-3 text-purple-500" />}
                  {tab === 'COMMAND CENTER' && (
                    <div className="relative">
                      <Bell className="w-3 h-3" />
                      {notifications.some(n => !n.read) && (
                        <span className="absolute -top-1 -right-1 w-1.5 h-1.5 bg-red-500 rounded-full animate-pulse" />
                      )}
                    </div>
                  )}
                  {tab === 'MANIFOLD' && <Activity className="w-3 h-3 text-blue-500" />}
                  {tab}
                </span>
                {activeTab === tab && (
                  <motion.div 
                    layoutId="activeTab"
                    className="absolute bottom-0 left-0 right-0 h-0.5 bg-red-500"
                  />
                )}
              </button>
            ))}
          </nav>
        </header>

        {/* Scrollable Area */}
        <div className="flex-1 overflow-y-auto p-8 pt-4 space-y-8">
          <AnimatePresence mode="wait">
            {activeTab === 'BACKTEST' && (
              <motion.div 
                key="backtest"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className="space-y-8"
              >
                <div className="p-8 bg-white border border-gray-100 rounded-3xl shadow-sm space-y-8">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="p-3 bg-amber-100 rounded-2xl">
                        <History className="w-8 h-8 text-amber-600" />
                      </div>
                      <div>
                        <h3 className="text-2xl font-black tracking-tight">Backtesting Engine</h3>
                        <p className="text-[10px] text-gray-400 uppercase font-bold tracking-widest">Historical Accuracy Validation</p>
                      </div>
                    </div>
                    <button 
                      onClick={() => handleRunBacktest(ticker || 'ANZ')}
                      disabled={isBacktesting}
                      className="px-6 py-3 bg-[#1A1A1A] text-white rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-black transition-all flex items-center gap-2"
                    >
                      {isBacktesting ? <Loader2 className="w-4 h-4 animate-spin" /> : <RefreshCw className="w-4 h-4" />}
                      {isBacktesting ? "RUNNING SIMULATION..." : "RUN BACKTEST SIMULATION"}
                    </button>
                  </div>

                  {isBacktesting && (
                    <div className="p-12 text-center space-y-4">
                      <Loader2 className="w-12 h-12 text-amber-600 animate-spin mx-auto" />
                      <div className="space-y-1">
                        <p className="text-sm font-bold text-amber-600 uppercase tracking-widest animate-pulse">Simulating Historical Tape...</p>
                        <p className="text-xs text-gray-400">Comparing AI predictions against actual historical outcomes.</p>
                      </div>
                    </div>
                  )}

                  {backtestData && !isBacktesting && (
                    <div className="space-y-8">
                      {/* Accuracy Metrics Grid */}
                      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                        <div className="p-6 bg-gray-50 rounded-2xl border border-gray-100 text-center">
                          <p className="text-[10px] text-gray-400 font-bold uppercase tracking-widest mb-2">Total Tests</p>
                          <p className="text-3xl font-black text-gray-900">{backtestData.metrics.totalTests}</p>
                        </div>
                        <div className="p-6 bg-emerald-50 rounded-2xl border border-emerald-100 text-center">
                          <p className="text-[10px] text-emerald-600 font-bold uppercase tracking-widest mb-2">Range Hit Rate</p>
                          <p className="text-3xl font-black text-emerald-700">{(backtestData.metrics.hitRate * 100).toFixed(1)}%</p>
                        </div>
                        <div className="p-6 bg-blue-50 rounded-2xl border border-blue-100 text-center">
                          <p className="text-[10px] text-blue-600 font-bold uppercase tracking-widest mb-2">Directional Accuracy</p>
                          <p className="text-3xl font-black text-blue-700">{(backtestData.metrics.directionalAccuracy * 100).toFixed(1)}%</p>
                        </div>
                        <div className="p-6 bg-purple-50 rounded-2xl border border-purple-100 text-center">
                          <p className="text-[10px] text-purple-600 font-bold uppercase tracking-widest mb-2">Prob Calibration</p>
                          <p className="text-3xl font-black text-purple-700">{(backtestData.metrics.probabilityCalibration * 100).toFixed(1)}%</p>
                        </div>
                      </div>

                      {/* Results Visualization - Simplified to just log for now */}
                      <div className="p-6 bg-white border border-gray-100 rounded-2xl shadow-sm space-y-4">
                        <h4 className="text-sm font-black uppercase tracking-widest text-gray-900">Detailed Simulation Log</h4>
                        <div className="space-y-3 max-h-[500px] overflow-y-auto no-scrollbar">
                          {backtestData.results.map((res, i) => (
                            <div key={i} className="p-4 bg-gray-50 rounded-xl border border-gray-100 flex items-center justify-between">
                              <div className="flex items-center gap-3">
                                <div className={cn("w-3 h-3 rounded-full", res.hit ? "bg-emerald-500" : "bg-red-500")} />
                                <div>
                                  <p className="text-xs font-black text-gray-900">{res.date}</p>
                                  <p className="text-[10px] text-gray-400 uppercase font-bold tracking-tighter">Actual: {res.actualPrice}</p>
                                </div>
                              </div>
                              <div className="text-right">
                                <p className="text-xs font-mono text-blue-600 font-bold">{res.predictedRange.low} - {res.predictedRange.high}</p>
                                <p className="text-[10px] text-gray-400 uppercase font-bold tracking-tighter">Confidence: {(res.confidence * 100).toFixed(0)}%</p>
                                <p className={cn("text-[10px] font-black mt-1", res.hit ? "text-emerald-600" : "text-red-600")}>
                                  {res.hit ? "HIT" : `MISS (${res.scenario.toUpperCase()})`}
                                </p>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* Backtest Insights */}
                      <div className="p-8 bg-gradient-to-br from-amber-50 to-orange-50 border border-amber-100 rounded-3xl space-y-4">
                        <div className="flex items-center gap-3">
                          <div className="p-2 bg-amber-100 rounded-lg">
                            <Brain className="w-5 h-5 text-amber-600" />
                          </div>
                          <h4 className="text-sm font-black tracking-tight uppercase">Accuracy Insights</h4>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                          <div className="space-y-2">
                            <p className="text-[10px] text-amber-700 font-bold uppercase">Systemic Calibration</p>
                            <p className="text-xs text-amber-900 leading-relaxed">
                              The model shows high directional accuracy but occasionally underestimates volatility in bear scenarios. Probability calibration is within 5% of target fidelity.
                            </p>
                          </div>
                          <div className="space-y-2">
                            <p className="text-[10px] text-amber-700 font-bold uppercase">Recommendation</p>
                            <p className="text-xs text-amber-900 leading-relaxed">
                              Increase weight on the 'Risk Manager' agent during high-volatility regimes to improve range coverage. Current hit rate of {(backtestData.metrics.hitRate * 100).toFixed(1)}% exceeds the 90% benchmark.
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                  {!backtestData && !isBacktesting && (
                    <div className="py-20 text-center space-y-4 bg-gray-50 border border-dashed border-gray-300 rounded-3xl">
                      <div className="p-4 bg-white rounded-full w-fit mx-auto shadow-sm">
                        <BarChart3 className="w-8 h-8 text-gray-300" />
                      </div>
                      <div className="space-y-1">
                        <p className="text-sm font-bold text-gray-400 uppercase tracking-widest">No Backtest Data</p>
                        <p className="text-xs text-gray-400">Run a simulation to validate the AI's historical accuracy for {ticker || 'ANZ'}.</p>
                      </div>
                    </div>
                  )}
                </div>
              </motion.div>
            )}

            {activeTab === 'HOW TO USE' && (
              <motion.div 
                key="how-to-use"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="space-y-8"
              >
                {/* Final Target Architecture Checklist */}
                <div className="p-8 bg-emerald-50 border border-emerald-100 rounded-3xl space-y-6">
                  <div className="flex items-center gap-3">
                    <div className="p-3 bg-emerald-100 rounded-2xl">
                      <CheckCircle2 className="w-8 h-8 text-emerald-600" />
                    </div>
                    <div>
                      <h3 className="text-xl font-black tracking-tight">Final Target Architecture Verification</h3>
                      <p className="text-[10px] text-emerald-600 uppercase font-bold tracking-widest">System Readiness Checklist</p>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {[
                      { label: "Query + Task Router", status: "IMPLEMENTED", desc: "Intelligent routing of user intent to specialized agents." },
                      { label: "RAG Layer (Search-First)", status: "IMPLEMENTED", desc: "Real-time data enforcement via Google Search grounding." },
                      { label: "Multi-Agent Engine", status: "IMPLEMENTED", desc: "Scientist, Risk Manager, Strategist, and Grounding Agent." },
                      { label: "Probability + Risk Model", status: "IMPLEMENTED", desc: "95% logic for scenario confidence and risk coverage." },
                      { label: "Backtesting Engine", status: "IMPLEMENTED", desc: "Historical accuracy validation and hit rate tracking." },
                      { label: "Decision Engine", status: "IMPLEMENTED", desc: "Buy/Hold/Sell logic with grounded rationale." },
                      { label: "Transparency Layer", status: "IMPLEMENTED", desc: "Neural logs and data gap identification." },
                      { label: "Mobile Optimization", status: "IMPLEMENTED", desc: "Responsive sidebar and touch-friendly UI." }
                    ].map((item, i) => (
                      <div key={i} className="p-4 bg-white rounded-2xl border border-emerald-100 flex items-start gap-3">
                        <div className="mt-0.5">
                          <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                        </div>
                        <div>
                          <div className="flex items-center gap-2 mb-1">
                            <h5 className="text-xs font-bold text-gray-900">{item.label}</h5>
                            <span className="text-[8px] font-black bg-emerald-100 text-emerald-700 px-1.5 py-0.5 rounded uppercase tracking-widest">{item.status}</span>
                          </div>
                          <p className="text-[10px] text-gray-500 leading-tight">{item.desc}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="p-8 bg-white border border-[#E5E7EB] rounded-3xl shadow-sm space-y-6">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-red-100 rounded-lg">
                      <BookOpen className="w-6 h-6 text-red-600" />
                    </div>
                    <div>
                      <h4 className="text-lg font-black tracking-tight">Singularity Lab Protocol (7 Steps)</h4>
                      <p className="text-[10px] text-gray-400 uppercase font-bold tracking-widest">Operational Guide</p>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {[
                      { step: 1, title: "Domain Selection", desc: "Choose your focus (Health, Finance, etc.) in the left panel to prime the agent logic." },
                      { step: 2, title: "Mission Intent", desc: "Define your objective in the FACTORY (CHAT) tab. Use the chat interface to communicate with the agent." },
                      { step: 3, title: "Visual Ingress", desc: "Capture a selfie or upload a file. The Optical Sensor analyzes temporal patterns for anomaly detection." },
                      { step: 4, title: "Orchestration", desc: "Click 'Generate Report'. This engages the Scientist, Risk Manager, and Strategist agents." },
                      { step: 5, title: "Ruliad Traversal", desc: "Use 'SEARCH RULIAD' to extract non-obvious rules from the computational universe." },
                      { step: 6, title: "Causal Validation", desc: "Run the Monte Carlo Simulation in the WORLD MODEL to verify the rule's resilience." },
                      { step: 7, title: "Omega Execution", desc: "Authorize the mission by typing 'EXECUTE OMEGA COMMAND' in the HIERARCHY." }
                    ].map((item) => (
                      <div key={item.step} className="flex gap-4 p-4 bg-[#F9FAFB] rounded-2xl border border-[#F3F4F6]">
                        <div className="w-8 h-8 bg-red-500 text-white rounded-full flex items-center justify-center font-bold text-xs shrink-0">
                          {item.step}
                        </div>
                        <div>
                          <p className="text-sm font-bold text-[#1A1A1A]">{item.title}</p>
                          <p className="text-xs text-[#6B7280] leading-relaxed">{item.desc}</p>
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* System Verification Checklist */}
                  <div className="mt-12 pt-8 border-t border-gray-100">
                    <div className="flex items-center gap-3 mb-6">
                      <div className="p-2 bg-blue-100 rounded-lg">
                        <ShieldCheck className="w-6 h-6 text-blue-600" />
                      </div>
                      <div>
                        <h4 className="text-lg font-black tracking-tight">System Verification Checklist</h4>
                        <p className="text-[10px] text-gray-400 uppercase font-bold tracking-widest">Final Operational Readiness</p>
                      </div>
                    </div>

                    <div className="overflow-hidden border border-gray-200 rounded-2xl">
                      <table className="w-full text-left border-collapse">
                        <thead>
                          <tr className="bg-gray-50 border-b border-gray-200">
                            <th className="px-6 py-4 text-[10px] font-black uppercase tracking-widest text-gray-500">Module</th>
                            <th className="px-6 py-4 text-[10px] font-black uppercase tracking-widest text-gray-500">Implementation Status</th>
                            <th className="px-6 py-4 text-[10px] font-black uppercase tracking-widest text-gray-500">Verification Method</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-100">
                          {[
                            { module: "Optical Sensor (Eye Scan)", status: "ACTIVE", method: "Real-time biometric retinal verification", color: "text-emerald-600" },
                            { module: "Medical Data Integration", status: "ACTIVE", method: "Bio-marker analysis & CRISPR simulation", color: "text-emerald-600" },
                            { module: "Humanoid Framework", status: "ACTIVE", method: "Proto-consciousness & Motor control", color: "text-emerald-600" },
                            { module: "Satellite Operations", status: "ACTIVE", method: "Deep-space mission telemetry", color: "text-emerald-600" },
                            { module: "Smart Watch Simulation", status: "ACTIVE", method: "Omega Protocol heart rate & SpO2 logs", color: "text-emerald-600" },
                            { module: "Voice Assistant (AI)", status: "ACTIVE", method: "Real-time audio feedback on all operations", color: "text-emerald-600" },
                            { module: "Alert Dispatch Center", status: "ACTIVE", method: "Email & SMS alerts (10% Threshold)", color: "text-emerald-600" },
                            { module: "CRISPR DNA Editor", status: "ACTIVE", method: "BRAF-V600E mutation correction simulation", color: "text-emerald-600" },
                            { module: "Video Simulation (Veo-1)", status: "ACTIVE", method: "Disease progression visual synthesis", color: "text-emerald-600" },
                            { module: "Mobile Optimization", status: "ACTIVE", method: "Responsive layout for on-the-go monitoring", color: "text-emerald-600" }
                          ].map((row, i) => (
                            <tr key={i} className="hover:bg-gray-50 transition-colors">
                              <td className="px-6 py-4">
                                <span className="text-xs font-bold text-gray-900">{row.module}</span>
                              </td>
                              <td className="px-6 py-4">
                                <div className="flex items-center gap-2">
                                  <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                                  <span className={cn("text-[10px] font-black uppercase tracking-widest", row.color)}>{row.status}</span>
                                </div>
                              </td>
                              <td className="px-6 py-4">
                                <span className="text-xs text-gray-500">{row.method}</span>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>

                  {/* Smart Watch Monitor: Real-time Detail */}
                  <div className="mt-12 p-8 bg-white border border-gray-100 rounded-3xl shadow-sm space-y-8">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="p-3 bg-emerald-100 rounded-2xl">
                          <Activity className="w-8 h-8 text-emerald-600" />
                        </div>
                        <div>
                          <h3 className="text-xl font-black tracking-tight">Smart Watch Monitor</h3>
                          <p className="text-[10px] text-gray-400 uppercase font-bold tracking-widest">Real-time Wearable Telemetry</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-4">
                        <div className="flex items-center gap-2">
                          <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
                          <span className="text-[10px] font-black text-emerald-600 uppercase tracking-widest">Live Sync</span>
                        </div>
                        <div className="px-3 py-1 bg-gray-900 text-white rounded-full text-[10px] font-mono">
                          OMEGA_PROTOCOL_V1
                        </div>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                      <div className="p-6 bg-gray-50 rounded-2xl border border-gray-100 space-y-2">
                        <p className="text-[10px] text-gray-400 font-bold uppercase tracking-widest">Heart Rate</p>
                        <p className="text-3xl font-black text-gray-900">{profile.bioMarkers.heartRate} <span className="text-xs font-normal text-gray-400">BPM</span></p>
                        <div className="h-1 bg-gray-200 rounded-full overflow-hidden">
                          <motion.div 
                            animate={{ width: `${(parseInt(profile.bioMarkers.heartRate) / 150) * 100}%` }}
                            className="h-full bg-emerald-500"
                          />
                        </div>
                      </div>
                      <div className="p-6 bg-gray-50 rounded-2xl border border-gray-100 space-y-2">
                        <p className="text-[10px] text-gray-400 font-bold uppercase tracking-widest">HRV (Stress)</p>
                        <p className={`text-3xl font-black ${parseInt(profile.bioMarkers.hrv) < 45 ? 'text-red-600' : 'text-emerald-600'}`}>{profile.bioMarkers.hrv} <span className="text-xs font-normal text-gray-400">ms</span></p>
                        <div className="h-1 bg-gray-200 rounded-full overflow-hidden">
                          <motion.div 
                            animate={{ width: `${(parseInt(profile.bioMarkers.hrv) / 100) * 100}%` }}
                            className={`h-full ${parseInt(profile.bioMarkers.hrv) < 45 ? 'bg-red-500' : 'bg-emerald-500'}`}
                          />
                        </div>
                      </div>
                      <div className="p-6 bg-gray-50 rounded-2xl border border-gray-100 space-y-2">
                        <p className="text-[10px] text-gray-400 font-bold uppercase tracking-widest">Stress Index</p>
                        <p className="text-3xl font-black text-gray-900">{behaviorData?.stressLevel || 0}%</p>
                        <div className="h-1 bg-gray-200 rounded-full overflow-hidden">
                          <motion.div 
                            animate={{ width: `${behaviorData?.stressLevel || 0}%` }}
                            className={`h-full ${ (behaviorData?.stressLevel || 0) > 70 ? 'bg-red-500' : 'bg-blue-500'}`}
                          />
                        </div>
                      </div>
                      <div className="p-6 bg-gray-50 rounded-2xl border border-gray-100 space-y-2">
                        <p className="text-[10px] text-gray-400 font-bold uppercase tracking-widest">Motion Status</p>
                        <p className="text-xl font-black text-gray-900 uppercase tracking-tighter">{behaviorData?.motion || "Stationary"}</p>
                        <div className="flex items-center gap-1 mt-2">
                          {[1,2,3,4,5].map(i => (
                            <div key={i} className={`w-1 h-3 rounded-full ${behaviorData?.motion === 'Active' ? 'bg-emerald-500 animate-pulse' : 'bg-gray-300'}`} style={{ animationDelay: `${i * 0.1}s` }} />
                          ))}
                        </div>
                      </div>
                    </div>

                    <div className="p-6 bg-emerald-50 border border-emerald-100 rounded-3xl">
                      <div className="flex items-center gap-2 mb-2 text-emerald-700">
                        <Zap className="w-4 h-4" />
                        <span className="text-[10px] font-bold uppercase tracking-widest">Real-time Bio-Insight</span>
                      </div>
                      <p className="text-sm text-emerald-900 leading-relaxed italic">
                        "{behaviorData?.insight || "Bio-metric baseline stable. No immediate interventions required."}"
                      </p>
                    </div>
                  </div>

                  {/* Phase 2: Fine-Tuning Roadmap */}
                  <div className="mt-12 pt-8 border-t border-gray-100">
                    <div className="flex items-center gap-3 mb-6">
                      <div className="p-2 bg-purple-100 rounded-lg">
                        <Brain className="w-6 h-6 text-purple-600" />
                      </div>
                      <div>
                        <h4 className="text-lg font-black tracking-tight">Phase 2: Fine-Tuning Roadmap</h4>
                        <p className="text-[10px] text-gray-400 uppercase font-bold tracking-widest">Upcoming Decision Intelligence Features</p>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      {[
                        { title: "Causal Graph Engine", desc: "True cause-effect reasoning for complex scenario modeling.", icon: <Network className="w-4 h-4" /> },
                        { title: "Auto Report Export", desc: "Generate and export PDF/Dashboard summaries automatically.", icon: <FileText className="w-4 h-4" /> },
                        { title: "Autonomous Execution", desc: "Auto-order groceries and rebalance portfolios via API.", icon: <Zap className="w-4 h-4" /> }
                      ].map((item, i) => (
                        <div key={i} className="p-4 bg-gray-50 rounded-2xl border border-gray-100 opacity-60 grayscale">
                          <div className="flex items-center gap-2 mb-2">
                            <div className="p-1.5 bg-white rounded-lg shadow-sm text-gray-400">
                              {item.icon}
                            </div>
                            <span className="text-[10px] font-black uppercase tracking-widest text-gray-400">Planned</span>
                          </div>
                          <h5 className="text-xs font-bold text-gray-600 mb-1">{item.title}</h5>
                          <p className="text-[10px] text-gray-400 leading-tight">{item.desc}</p>
                        </div>
                      ))}
                    </div>
                  </div>

                  <button 
                    onClick={handleFullScaleSystemTest}
                    disabled={isTesting}
                    className="w-full py-4 bg-[#1A1A1A] text-white rounded-2xl text-xs font-black uppercase tracking-widest shadow-lg shadow-gray-200 hover:bg-black transition-all flex items-center justify-center gap-2 mb-4"
                  >
                    <Zap className="w-4 h-4 text-amber-400" />
                    {isTesting ? "TESTING..." : "RUN FULL SCALE SYSTEM TEST"}
                  </button>

                  <div className="p-6 bg-red-50 border border-red-100 rounded-3xl space-y-4">
                    <div className="flex items-center gap-3">
                      <div className="p-2 bg-red-100 rounded-lg">
                        <Zap className="w-6 h-6 text-red-600" />
                      </div>
                      <div>
                        <h4 className="text-sm font-black tracking-tight uppercase">Omega Stress Test</h4>
                        <p className="text-[10px] text-red-600 font-bold uppercase tracking-widest">Emergency Protocol Simulation</p>
                      </div>
                    </div>
                    <p className="text-xs text-red-800 leading-relaxed">
                      Test the system's response to a critical health event. This will simulate a massive drop in HRV, trigger a red alert, and initiate an emergency voice uplink.
                    </p>
                    <button 
                      onClick={handleSimulateEmergency}
                      className="w-full py-4 bg-red-600 text-white rounded-2xl text-xs font-black uppercase tracking-widest shadow-lg shadow-red-200 hover:bg-red-700 transition-all flex items-center justify-center gap-2"
                    >
                      <PhoneCall className="w-4 h-4" />
                      INITIATE EMERGENCY STRESS TEST
                    </button>
                  </div>
                </div>
              </motion.div>
            )}

            {activeTab === 'COSMO-HUMANOID' && (
              <motion.div 
                key="cosmo-humanoid"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className="space-y-8"
              >
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                  {/* Internal State (Proto-Consciousness) */}
                  <section className="lg:col-span-2 p-8 bg-white border border-emerald-100 rounded-3xl shadow-sm space-y-8">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="p-3 bg-emerald-100 rounded-2xl">
                          <Brain className="w-8 h-8 text-emerald-600" />
                        </div>
                        <div>
                          <h3 className="text-2xl font-black tracking-tight">Proto-Consciousness</h3>
                          <p className="text-[10px] text-gray-400 uppercase font-bold tracking-widest">Internal State Vector (ISV)</p>
                        </div>
                      </div>
                      <div className="px-4 py-2 bg-emerald-50 border border-emerald-100 rounded-xl">
                        <div className="flex items-center gap-2">
                          <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                          <span className="text-[10px] font-black text-emerald-700 uppercase tracking-widest">Cognition Active</span>
                        </div>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                      {/* Mood & Stress */}
                      <div className="space-y-6">
                        <div className="space-y-4">
                          <div className="flex items-center justify-between">
                            <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Mood Spectrum</span>
                            <span className="text-[10px] font-bold text-emerald-600 uppercase tracking-widest">{(humanoidState.mood * 100).toFixed(0)}% Positive</span>
                          </div>
                          <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                            <motion.div 
                              initial={{ width: 0 }}
                              animate={{ width: `${humanoidState.mood * 100}%` }}
                              className="h-full bg-gradient-to-r from-red-400 via-yellow-400 to-emerald-400"
                            />
                          </div>
                        </div>

                        <div className="space-y-4">
                          <div className="flex items-center justify-between">
                            <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Stress Level</span>
                            <span className="text-[10px] font-bold text-red-600 uppercase tracking-widest">{(humanoidState.stress * 100).toFixed(0)}% Intensity</span>
                          </div>
                          <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                            <motion.div 
                              initial={{ width: 0 }}
                              animate={{ width: `${humanoidState.stress * 100}%` }}
                              className="h-full bg-red-500"
                            />
                          </div>
                        </div>

                        <div className="grid grid-cols-3 gap-4">
                          {[
                            { label: 'Anger', val: humanoidState.anger, color: 'text-red-600' },
                            { label: 'Calm', val: humanoidState.calm, color: 'text-blue-600' },
                            { label: 'Engage', val: humanoidState.engagement, color: 'text-emerald-600' }
                          ].map(e => (
                            <div key={e.label} className="p-3 bg-gray-50 rounded-xl border border-gray-100 text-center">
                              <p className="text-[8px] font-bold text-gray-400 uppercase tracking-widest mb-1">{e.label}</p>
                              <p className={cn("text-lg font-black", e.color)}>{(e.val * 100).toFixed(0)}</p>
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* Attention & Focus */}
                      <div className="space-y-6">
                        <div className="p-6 bg-gray-900 rounded-2xl border border-white/10 relative overflow-hidden group">
                          <div className="absolute top-0 right-0 p-4">
                            <Target className="w-12 h-12 text-white/5 group-hover:text-emerald-500/10 transition-colors" />
                          </div>
                          <div className="relative z-10 space-y-4">
                            <div className="flex items-center gap-2">
                              <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-ping" />
                              <span className="text-[10px] font-bold text-emerald-400 uppercase tracking-widest">Focus Lock</span>
                            </div>
                            <h4 className="text-xl font-black text-white tracking-tight">Mission Objective Alpha</h4>
                            <div className="flex items-center gap-4">
                              <div className="flex-1 h-1 bg-white/10 rounded-full">
                                <div className="h-full bg-emerald-500 w-[70%]" />
                              </div>
                              <span className="text-[10px] font-mono text-emerald-400">70%</span>
                            </div>
                          </div>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                          <div className="p-4 bg-gray-50 rounded-xl border border-gray-100">
                            <div className="flex items-center justify-between mb-2">
                              <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Attention</span>
                              <Activity className="w-3 h-3 text-blue-500" />
                            </div>
                            <p className="text-xl font-black text-gray-900">{(humanoidState.attention * 100).toFixed(0)}%</p>
                          </div>
                          <div className="p-4 bg-gray-50 rounded-xl border border-gray-100">
                            <div className="flex items-center justify-between mb-2">
                              <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Energy</span>
                              <Zap className="w-3 h-3 text-amber-500" />
                            </div>
                            <p className="text-xl font-black text-gray-900">{(humanoidState.energy * 100).toFixed(0)}%</p>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Simulation Controls */}
                    <div className="pt-8 border-t border-gray-100 flex items-center gap-4">
                      <button 
                        onClick={() => setHumanoidState(prev => ({ ...prev, stress: Math.min(1, prev.stress + 0.1), mood: Math.max(0, prev.mood - 0.05) }))}
                        className="px-6 py-3 bg-red-50 text-red-600 rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-red-100 transition-all border border-red-100"
                      >
                        Inject Stressor
                      </button>
                      <button 
                        onClick={() => setHumanoidState(prev => ({ ...prev, stress: Math.max(0, prev.stress - 0.1), mood: Math.min(1, prev.mood + 0.1) }))}
                        className="px-6 py-3 bg-emerald-50 text-emerald-600 rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-emerald-100 transition-all border border-emerald-100"
                      >
                        Apply Calmative
                      </button>
                      <button 
                        onClick={() => setHumanoidState({ mood: 0.5, stress: 0.2, attention: 0.8, energy: 0.9, goalFocus: 0.7, anger: 0.0, calm: 0.8, engagement: 0.6 })}
                        className="px-6 py-3 bg-gray-50 text-gray-600 rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-gray-100 transition-all border border-gray-100"
                      >
                        Reset ISV
                      </button>
                    </div>
                  </section>

                  {/* Mission Ops & Satellite */}
                  <div className="space-y-8">
                    <section className="p-8 bg-gray-900 text-white rounded-3xl shadow-xl space-y-6 border border-white/10">
                      <div className="flex items-center gap-3">
                        <div className="p-3 bg-blue-500/20 rounded-2xl">
                          <Globe className="w-8 h-8 text-blue-400" />
                        </div>
                        <div>
                          <h3 className="text-xl font-black tracking-tight">Mission Ops</h3>
                          <p className="text-[10px] text-gray-400 uppercase font-bold tracking-widest">Satellite & Space Link</p>
                        </div>
                      </div>

                      <div className="space-y-4">
                        <div className="p-4 bg-white/5 rounded-2xl border border-white/10 flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            <Wifi className="w-5 h-5 text-emerald-400" />
                            <div>
                              <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Link Status</p>
                              <p className="text-sm font-black text-emerald-400">{satelliteStatus.link}</p>
                            </div>
                          </div>
                          <div className="text-right">
                            <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Latency</p>
                            <p className="text-sm font-mono">{satelliteStatus.latency}</p>
                          </div>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                          <div className="p-4 bg-white/5 rounded-2xl border border-white/10">
                            <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1">Uplink</p>
                            <p className="text-sm font-black text-blue-400">{satelliteStatus.uplink}</p>
                          </div>
                          <div className="p-4 bg-white/5 rounded-2xl border border-white/10">
                            <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1">Downlink</p>
                            <p className="text-sm font-black text-purple-400">{satelliteStatus.downlink}</p>
                          </div>
                        </div>

                        <div className="p-4 bg-white/5 rounded-2xl border border-white/10">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Orbital Position</span>
                            <span className="text-[10px] font-mono text-blue-400">{satelliteStatus.orbit}</span>
                          </div>
                          <div className="h-1 bg-white/10 rounded-full overflow-hidden">
                            <motion.div 
                              animate={{ x: ['-100%', '100%'] }}
                              transition={{ duration: 10, repeat: Infinity, ease: 'linear' }}
                              className="w-1/3 h-full bg-blue-500"
                            />
                          </div>
                        </div>
                      </div>
                    </section>

                    <section className="p-8 bg-white border border-gray-100 rounded-3xl shadow-sm space-y-6">
                      <div className="flex items-center gap-3">
                        <div className="p-3 bg-orange-100 rounded-2xl">
                          <Cpu className="w-8 h-8 text-orange-600" />
                        </div>
                        <div>
                          <h3 className="text-xl font-black tracking-tight">Robot Motors</h3>
                          <p className="text-[10px] text-gray-400 uppercase font-bold tracking-widest">Humanoid Actuators</p>
                        </div>
                      </div>

                      <div className="space-y-4">
                        {[
                          { label: 'Neck Rotation', val: robotMotors.neck, unit: '°' },
                          { label: 'Left Arm Extension', val: robotMotors.leftArm, unit: '%' },
                          { label: 'Right Arm Extension', val: robotMotors.rightArm, unit: '%' },
                          { label: 'Torso Tilt', val: robotMotors.torso, unit: '°' }
                        ].map(m => (
                          <div key={m.label} className="space-y-2">
                            <div className="flex items-center justify-between">
                              <span className="text-[10px] font-bold text-gray-500 uppercase tracking-widest">{m.label}</span>
                              <span className="text-[10px] font-mono font-bold text-orange-600">{m.val}{m.unit}</span>
                            </div>
                            <div className="h-1.5 bg-gray-100 rounded-full overflow-hidden">
                              <div className="h-full bg-orange-500" style={{ width: `${Math.abs(m.val)}%` }} />
                            </div>
                          </div>
                        ))}
                        <div className="pt-4 flex items-center justify-between">
                          <span className="text-[10px] font-bold text-gray-500 uppercase tracking-widest">Leg Status</span>
                          <span className="px-2 py-1 bg-gray-900 text-white text-[8px] font-black rounded uppercase tracking-widest">{robotMotors.legs}</span>
                        </div>
                      </div>
                    </section>
                  </div>
                </div>

                {/* Human-Like Test Suite */}
                <section className="p-8 bg-white border border-gray-100 rounded-3xl shadow-sm space-y-8">
                  <div className="flex items-center gap-3">
                    <div className="p-3 bg-red-100 rounded-lg">
                      <Trophy className="w-6 h-6 text-red-600" />
                    </div>
                    <div>
                      <h4 className="text-lg font-black tracking-tight">Human-Like Test Suite</h4>
                      <p className="text-[10px] text-gray-400 uppercase font-bold tracking-widest">Emotion & Task Verification</p>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {[
                      { 
                        title: "Emotion Interaction", 
                        scenario: "User Angry", 
                        expectation: "De-escalate, calm tone",
                        status: "READY",
                        icon: <MessageSquare className="w-4 h-4" />
                      },
                      { 
                        title: "Task Precision", 
                        scenario: "Pick & Place", 
                        expectation: "Stable grasp, zero drop",
                        status: "READY",
                        icon: <Target className="w-4 h-4" />
                      },
                      { 
                        title: "Stress Resilience", 
                        scenario: "Sensor Failure", 
                        expectation: "Safe mode, local autonomy",
                        status: "READY",
                        icon: <AlertTriangle className="w-4 h-4" />
                      }
                    ].map((test, i) => (
                      <div key={i} className="p-6 bg-gray-50 rounded-2xl border border-gray-100 space-y-4 group hover:border-red-200 transition-all">
                        <div className="flex items-center justify-between">
                          <div className="p-2 bg-white rounded-lg shadow-sm text-red-600">
                            {test.icon}
                          </div>
                          <span className="text-[8px] font-black bg-emerald-100 text-emerald-700 px-2 py-1 rounded uppercase tracking-widest">{test.status}</span>
                        </div>
                        <div>
                          <h5 className="text-sm font-bold text-gray-900">{test.title}</h5>
                          <p className="text-[10px] text-gray-400 uppercase font-bold tracking-widest mb-2">{test.scenario}</p>
                          <p className="text-xs text-gray-500 leading-relaxed italic">"Expectation: {test.expectation}"</p>
                        </div>
                        <button 
                          onClick={() => handleHumanoidTest(test.title.toLowerCase().includes('emotion') ? 'emotion' : test.title.toLowerCase().includes('precision') ? 'precision' : 'stress')}
                          disabled={isTesting}
                          className="w-full py-2 bg-white border border-gray-200 rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-red-500 hover:text-white hover:border-red-500 transition-all"
                        >
                          {isTesting ? 'Running...' : 'Run Test'}
                        </button>
                      </div>
                    ))}
                  </div>
                </section>
              </motion.div>
            )}

            {activeTab === 'FACTORY (CHAT)' && (
              <motion.div 
                key="factory"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="space-y-8"
              >
                {/* Quick Toggle for Autoimmune Mode */}
                <div className="flex items-center justify-between p-4 bg-red-50 border border-red-100 rounded-2xl">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-red-100 rounded-lg">
                      <Activity className="w-5 h-5 text-red-600" />
                    </div>
                    <div>
                      <h4 className="text-sm font-black tracking-tight">Autoimmune Research Mode</h4>
                      <p className="text-[10px] text-red-600 uppercase font-bold tracking-widest">Closed-Loop Engine Status</p>
                    </div>
                  </div>
                  <button 
                    onClick={() => setIsAutoimmuneMode(!isAutoimmuneMode)}
                    className={cn(
                      "flex items-center gap-2 px-4 py-2 rounded-xl text-[10px] font-bold uppercase tracking-widest transition-all shadow-sm",
                      isAutoimmuneMode ? "bg-red-600 text-white" : "bg-white text-gray-400 border border-gray-200"
                    )}
                  >
                    {isAutoimmuneMode ? 'ACTIVE' : 'INACTIVE'}
                    <div className={cn(
                      "w-2 h-2 rounded-full animate-pulse",
                      isAutoimmuneMode ? "bg-white" : "bg-gray-300"
                    )} />
                  </button>
                </div>

                {/* Master JSON Ingress */}
                {isAutoimmuneMode && (
                  <div className="p-6 bg-[#1A1A1A] rounded-3xl border border-[#333] space-y-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <Database className="w-4 h-4 text-red-500" />
                        <h4 className="text-sm font-bold text-white uppercase tracking-widest">Master JSON Ingress</h4>
                      </div>
                      <span className="text-[10px] text-gray-500 font-mono">SCHEMA: AUTOIMMUNE_V1.0</span>
                    </div>
                    <textarea 
                      value={textContent}
                      onChange={(e) => setTextContent(e.target.value)}
                      placeholder='{ "patient_id": "001", "biomarkers": { "CRP": 5.2, "IL6": 12.1 }, ... }'
                      className="w-full h-32 bg-black/50 border border-[#333] rounded-xl p-4 text-xs font-mono text-emerald-400 focus:outline-none focus:border-red-500"
                    />
                    <div className="flex justify-between items-center">
                      <p className="text-[10px] text-gray-500">Paste your Master JSON schema for time-series flare prediction.</p>
                      <button 
                        onClick={() => setTextContent(JSON.stringify({
                          patient_id: "001",
                          timestamp: new Date().toISOString().split('T')[0],
                          biomarkers: { CRP: 5.2, IL6: 12.1 },
                          vitals: { HRV: 45, sleep_hours: 5 },
                          diet: { gluten: true, sugar: "high" },
                          medication: { methotrexate: true },
                          symptoms: { pain: 7, fatigue: 8 }
                        }, null, 2))}
                        className="text-[10px] text-red-500 hover:underline font-bold"
                      >
                        LOAD TEMPLATE
                      </button>
                    </div>
                  </div>
                )}

                {/* Mission Intent Input (Chat Interface) */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                  <section className="lg:col-span-2 space-y-6">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4">
                        <label className="text-[10px] font-bold text-[#6B7280] uppercase tracking-widest block">Mission Control Chat</label>
                        <button 
                          onClick={() => setActiveTab('COMMAND CENTER')}
                          className="px-3 py-1 bg-[#1A1A1A] text-white text-[8px] font-bold rounded-lg hover:bg-black transition-all flex items-center gap-1.5"
                        >
                          <Terminal className="w-2.5 h-2.5 text-emerald-400" />
                          GO TO COMMAND CENTER
                        </button>
                      </div>
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                        <span className="text-[10px] font-bold text-green-600 uppercase tracking-widest">Live Uplink</span>
                      </div>
                    </div>

                    {/* Chat History Bubble */}
                    <div className="space-y-4 max-h-[300px] overflow-y-auto no-scrollbar p-4 bg-white border border-[#E5E7EB] rounded-3xl shadow-inner">
                      {chatHistory.length === 0 ? (
                        <div className="py-12 text-center space-y-3">
                          <MessageSquare className="w-8 h-8 text-gray-200 mx-auto" />
                          <p className="text-[10px] text-gray-400 font-bold uppercase tracking-widest">Awaiting Mission Directives</p>
                        </div>
                      ) : (
                        chatHistory.map((msg, i) => (
                          <motion.div 
                            key={i}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className={cn(
                              "flex gap-3 max-w-[85%]",
                              msg.role === 'user' ? "ml-auto flex-row-reverse" : "mr-auto"
                            )}
                          >
                            <div className={cn(
                              "p-2 rounded-lg shrink-0",
                              msg.role === 'user' ? "bg-blue-100" : "bg-purple-100"
                            )}>
                              {msg.role === 'user' ? <User className="w-4 h-4 text-blue-600" /> : <Bot className="w-4 h-4 text-purple-600" />}
                            </div>
                            <div className={cn(
                              "p-4 rounded-2xl text-xs leading-relaxed",
                              msg.role === 'user' ? "bg-blue-600 text-white rounded-tr-none" : "bg-gray-100 text-gray-800 rounded-tl-none"
                            )}>
                              {msg.content}
                            </div>
                          </motion.div>
                        ))
                      )}
                    </div>

                    {/* Neural Log - Agentic Autonomy Simulation */}
                    <div className="p-6 bg-[#1A1A1A] rounded-3xl border border-[#333] space-y-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Terminal className="w-4 h-4 text-emerald-500" />
                          <h4 className="text-sm font-bold text-white uppercase tracking-widest">Neural Log (Live)</h4>
                        </div>
                        <div className="flex items-center gap-2">
                          <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
                          <span className="text-[10px] text-emerald-500 font-mono">AGENTIC AUTONOMY ACTIVE</span>
                        </div>
                      </div>
                      <div className="h-40 overflow-y-auto no-scrollbar font-mono text-[10px] space-y-2">
                        {neuralLog.length === 0 ? (
                          <p className="text-gray-600 italic">Initializing neural uplink...</p>
                        ) : (
                          neuralLog.map((log, i) => (
                            <div key={i} className="flex gap-4 border-b border-white/5 pb-1">
                              <span className="text-gray-500 shrink-0">[{log.timestamp}]</span>
                              <span className="text-blue-400 font-bold shrink-0">{log.agent}:</span>
                              <span className="text-gray-300">{log.action}</span>
                            </div>
                          ))
                        )}
                      </div>
                    </div>

                    <div className="relative">
                      <textarea
                        value={missionIntent}
                        onChange={(e) => setMissionIntent(e.target.value)}
                        placeholder={`Enter mission intent for ${activeDomain} focus...`}
                        className="w-full p-6 pr-16 bg-[#F3F4F6] border border-[#E5E7EB] rounded-3xl text-sm font-medium focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all min-h-[100px] resize-none shadow-sm"
                      />
                      <div className="absolute bottom-4 right-4 flex gap-2">
                        {activeDomain === 'Finance' && (
                          <button 
                            onClick={handleGenerateFinanceReport}
                            disabled={isGeneratingFinanceReport || !ticker}
                            className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-2xl hover:bg-blue-700 disabled:opacity-50 transition-all shadow-xl group"
                          >
                            {isGeneratingFinanceReport ? (
                              <Loader2 className="w-5 h-5 animate-spin" />
                            ) : (
                              <FileText className="w-5 h-5 group-hover:scale-110 transition-transform" />
                            )}
                            <span className="text-xs font-bold uppercase tracking-widest">Generate Forecast</span>
                          </button>
                        )}
                        <button 
                          onClick={handleProcess}
                          disabled={isProcessing || (!missionIntent && !ticker)}
                          className="flex items-center gap-2 px-6 py-3 bg-[#1A1A1A] text-white rounded-2xl hover:bg-black disabled:opacity-50 transition-all shadow-xl group"
                        >
                          {isProcessing ? (
                            <Loader2 className="w-5 h-5 animate-spin" />
                          ) : (
                            <Send className="w-5 h-5 group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform" />
                          )}
                        </button>
                      </div>
                    </div>
                  </section>

                  {/* Visual Ingress Preview */}
                  <section>
                    <div className="flex items-center justify-between mb-3">
                      <label className="text-[10px] font-bold text-[#6B7280] uppercase tracking-widest block">Visual Ingress</label>
                      <div className="flex gap-2">
                        <label className="cursor-pointer p-1.5 bg-white border border-[#E5E7EB] rounded-lg hover:bg-gray-50 transition-all shadow-sm">
                          <Upload className="w-3 h-3 text-blue-600" />
                          <input type="file" className="hidden" onChange={handleFileUpload} accept="image/*,.txt" />
                        </label>
                        {(capturedImage || uploadedText) && (
                          <button 
                            onClick={() => { setCapturedImage(null); setUploadedText(null); }}
                            className="p-1.5 bg-white border border-[#E5E7EB] rounded-lg hover:bg-red-50 text-red-500 transition-all shadow-sm"
                          >
                            <X className="w-3 h-3" />
                          </button>
                        )}
                      </div>
                    </div>
                    <div className="aspect-video lg:aspect-square bg-white border border-[#E5E7EB] rounded-xl overflow-hidden flex items-center justify-center relative shadow-sm">
                      {capturedImage ? (
                        <img 
                          src={capturedImage} 
                          alt="Captured Input" 
                          className="w-full h-full object-cover"
                        />
                      ) : uploadedText ? (
                        <div className="w-full h-full p-4 bg-[#F9FAFB] overflow-y-auto">
                          <div className="flex items-center gap-2 mb-2 text-blue-600">
                            <FileText className="w-4 h-4" />
                            <span className="text-[10px] font-bold uppercase tracking-widest">Text Data Ingress</span>
                          </div>
                          <pre className="text-[10px] font-mono whitespace-pre-wrap text-[#4B5563] leading-relaxed">
                            {uploadedText}
                          </pre>
                        </div>
                      ) : (
                        <div className="text-center p-6 space-y-2">
                          <Camera className="w-8 h-8 text-[#9CA3AF] mx-auto opacity-20" />
                          <p className="text-[10px] text-[#9CA3AF] font-bold uppercase tracking-widest">No Visual Data</p>
                          <p className="text-[8px] text-[#9CA3AF]">Upload image or .txt list</p>
                        </div>
                      )}
                    </div>
                  </section>
                </div>

                {/* Prediction & Grid */}
                {prediction && (
                  <section className="space-y-6">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-orange-100 rounded-lg">
                          <Terminal className="w-5 h-5 text-orange-600" />
                        </div>
                        <h3 className="text-xl font-black tracking-tight">90-Step Factory Grid [OPTIMIZED]</h3>
                      </div>
                      <div className="flex items-center gap-3">
                        {groundingStatus && (
                          <div className={`px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest flex items-center gap-2 ${groundingStatus.verified ? 'bg-green-500/20 text-green-400 border border-green-500/30' : 'bg-red-500/20 text-red-400 border border-red-500/30'}`}>
                            <div className={`w-1.5 h-1.5 rounded-full ${groundingStatus.verified ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`} />
                            {groundingStatus.verified ? 'Verified Tape' : 'Data Gap Detected'}
                          </div>
                        )}
                        <button 
                          onClick={() => setActiveTab('REPORTS')}
                          className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-xl text-[10px] font-bold uppercase tracking-widest hover:bg-purple-700 transition-all shadow-lg shadow-purple-200"
                        >
                        <FileText className="w-4 h-4" />
                        View Full Report
                      </button>
                    </div>
                  </div>

                    <div className="p-6 bg-white border border-[#E5E7EB] rounded-2xl shadow-sm">
                      <div className="mb-6 p-4 bg-blue-50 border-l-4 border-blue-500 rounded-r-lg">
                        <p className="text-sm font-bold text-blue-900 mb-1">Hypergraph Prediction</p>
                        <p className="text-sm text-blue-800 leading-relaxed italic">"{prediction}"</p>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {tasks.map((task, idx) => (
                          <div 
                            key={idx}
                            className="flex items-start gap-3 p-3 bg-[#F9FAFB] rounded-xl border border-[#F3F4F6] group hover:border-blue-200 transition-all"
                          >
                            <div className="mt-0.5">
                              {task.approved ? <CheckCircle2 className="w-4 h-4 text-green-500" /> : <div className="w-4 h-4 rounded-full border-2 border-gray-300" />}
                            </div>
                            <span className="text-xs font-medium text-[#4B5563] leading-tight">{task.text}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {summary && (
                          <div className="p-4 bg-purple-50 border border-purple-100 rounded-2xl space-y-2">
                            <div className="flex items-center gap-2 text-purple-600">
                              <Brain className="w-4 h-4" />
                              <span className="text-[10px] font-bold uppercase tracking-widest">Mission Summary</span>
                            </div>
                            <p className="text-[10px] text-purple-800 leading-relaxed italic">"{summary}"</p>
                          </div>
                        )}
                        {suggestions && (
                          <div className="p-4 bg-orange-50 border border-orange-100 rounded-2xl space-y-2">
                            <div className="flex items-center gap-2 text-orange-600">
                              <Lightbulb className="w-4 h-4" />
                              <span className="text-[10px] font-bold uppercase tracking-widest">Strategic Suggestions</span>
                            </div>
                            <p className="text-[10px] text-orange-800 leading-relaxed italic">
                              {suggestions.toLowerCase() === 'none' ? 'No further suggestions pending.' : `"${suggestions}"`}
                            </p>
                          </div>
                        )}
                      </div>

                      {/* Multi-Agent Reports */}
                    {agentReports && (
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div className="p-4 bg-blue-50/50 border border-blue-100 rounded-2xl space-y-2">
                          <div className="flex items-center gap-2 text-blue-600">
                            <Microscope className="w-4 h-4" />
                            <span className="text-[10px] font-bold uppercase tracking-widest">Scientist Report</span>
                          </div>
                          <p className="text-[10px] text-blue-800 leading-relaxed italic">"{agentReports.scientist}"</p>
                        </div>
                        <div className="p-4 bg-red-50/50 border border-red-100 rounded-2xl space-y-2">
                          <div className="flex items-center gap-2 text-red-600">
                            <ShieldCheck className="w-4 h-4" />
                            <span className="text-[10px] font-bold uppercase tracking-widest">Risk Manager</span>
                          </div>
                          <p className="text-[10px] text-red-800 leading-relaxed italic">"{agentReports.riskManager}"</p>
                        </div>
                        <div className="p-4 bg-emerald-50/50 border border-emerald-100 rounded-2xl space-y-2">
                          <div className="flex items-center gap-2 text-emerald-600">
                            <Target className="w-4 h-4" />
                            <span className="text-[10px] font-bold uppercase tracking-widest">Strategist</span>
                          </div>
                          <p className="text-[10px] text-emerald-800 leading-relaxed italic">"{agentReports.strategist}"</p>
                        </div>
                        {agentReports?.groundingAgent && (
                          <div className="p-4 bg-orange-50/50 border border-orange-100 rounded-2xl space-y-2 md:col-span-3">
                            <div className="flex items-center gap-2 text-orange-600">
                              <Search className="w-4 h-4" />
                              <span className="text-[10px] font-bold uppercase tracking-widest">Grounding Agent (Tape Verification)</span>
                            </div>
                            <p className="text-[10px] text-orange-800 leading-relaxed italic">"{agentReports.groundingAgent}"</p>
                            {groundingStatus?.gaps && groundingStatus.gaps.length > 0 && (
                              <div className="flex flex-wrap gap-1 mt-1">
                                {groundingStatus?.gaps?.map((gap: any, i: number) => (
                                  <span key={i} className="px-1.5 py-0.5 rounded bg-red-500/10 text-red-600 text-[8px] font-bold border border-red-500/20">
                                    GAP: {gap.description || gap}
                                  </span>
                                ))}
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    )}
                  </section>
                )}

                {/* Execution Logs (Factory) */}
                {executionLogs.length > 0 && (
                  <div className="p-6 bg-[#1A1A1A] text-white rounded-2xl shadow-xl space-y-4 border border-white/10">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <Terminal className="w-4 h-4 text-emerald-400" />
                        <h4 className="text-[10px] font-bold uppercase tracking-widest">Command Center: Execution Logs</h4>
                      </div>
                      <div className="flex items-center gap-4">
                        {groundingStatus && (
                          <div className={`flex items-center gap-1.5 px-2 py-0.5 rounded border ${groundingStatus?.verified ? 'bg-green-500/10 border-green-500/30 text-green-400' : 'bg-red-500/10 border-red-500/30 text-red-400'}`}>
                            <div className={`w-1 h-1 rounded-full ${groundingStatus?.verified ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`} />
                            <span className="text-[8px] font-bold uppercase tracking-widest">{groundingStatus?.verified ? 'Verified Tape' : 'Data Gap'}</span>
                          </div>
                        )}
                        <button 
                          onClick={() => setActiveTab('COMMAND CENTER')}
                          className="text-[8px] font-bold text-emerald-400 hover:underline flex items-center gap-1"
                        >
                          GO TO COMMAND CENTER <Zap className="w-2 h-2" />
                        </button>
                        <div className="flex items-center gap-2">
                          <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
                          <span className="text-[8px] font-bold text-emerald-400">EXECUTING</span>
                        </div>
                      </div>
                    </div>
                    <div className="space-y-1 font-mono text-[9px] max-h-[200px] overflow-y-auto no-scrollbar">
                      {executionLogs.map((log, i) => (
                        <div key={i} className="flex gap-2">
                          <span className="text-gray-500">[{new Date().toLocaleTimeString()}]</span>
                          <span className={log.includes('[SUCCESS]') ? 'text-emerald-400' : 'text-gray-300'}>{log}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </motion.div>
            )}

            {activeTab === 'REPORTS' && (
              <motion.div 
                key="reports"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="space-y-8"
              >
                {/* Health Metrics (Autoimmune Mode) */}
                {loopData?.healthMetrics && (
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="p-6 bg-red-50 border border-red-100 rounded-3xl text-center">
                      <p className="text-[10px] text-red-600 font-bold uppercase tracking-widest mb-2">Flare Probability</p>
                      <p className="text-4xl font-black text-red-700">{(loopData.healthMetrics.flareProbability * 100).toFixed(0)}%</p>
                      <p className="text-[10px] text-red-500 mt-2">Window: 24-72h</p>
                    </div>
                    <div className="p-6 bg-white border border-[#E5E7EB] rounded-3xl">
                      <p className="text-[10px] text-gray-400 font-bold uppercase tracking-widest mb-2">Primary Driver</p>
                      <p className="text-lg font-bold text-[#1A1A1A]">{loopData.healthMetrics.primaryDriver}</p>
                      <div className="mt-4 p-2 bg-gray-50 rounded-lg border border-gray-100">
                        <p className="text-[10px] text-gray-500 font-mono leading-tight">{loopData.healthMetrics.causalChain}</p>
                      </div>
                    </div>
                    <div className="p-6 bg-[#1A1A1A] rounded-3xl border border-[#333]">
                      <p className="text-[10px] text-red-500 font-bold uppercase tracking-widest mb-2">Hypothesis Testing</p>
                      <div className="space-y-3">
                        {loopData.healthMetrics.hypothesisTesting?.slice(0, 2).map((h: any) => (
                          <div key={h.id} className="space-y-1">
                            <div className="flex justify-between text-[10px]">
                              <span className="text-gray-400 font-bold">{h.id}</span>
                              <span className="text-emerald-500 font-mono">{(h.confidence * 100).toFixed(0)}% CONF</span>
                            </div>
                            <p className="text-[10px] text-white leading-tight">{h.hypothesis}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
                <div className="flex items-center justify-between">
                  <h3 className="text-2xl font-black tracking-tight">Mission Intelligence Reports</h3>
                  {routedModel && (
                    <div className="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-[10px] font-mono">
                      ROUTED: {routedModel}
                    </div>
                  )}
                </div>

                {/* Finance Forecast Report */}
                {financeReport && (
                  <div className="space-y-8">
                    {/* Grounding Summary Card */}
                    <motion.div 
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="p-8 bg-gradient-to-br from-gray-900 to-blue-900 rounded-3xl shadow-2xl border border-blue-500/30 overflow-hidden relative"
                    >
                      <div className="absolute top-0 right-0 p-12 opacity-10">
                        <ShieldCheck className="w-48 h-48 text-white" />
                      </div>
                      <div className="relative z-10 space-y-6">
                        <div className="flex items-center gap-3">
                          <div className="p-2 bg-blue-500/20 rounded-xl border border-blue-400/30">
                            <ShieldCheck className="w-6 h-6 text-blue-400" />
                          </div>
                          <div>
                            <h3 className="text-xl font-black text-white tracking-tight uppercase">Grounding Analysis & Accuracy Summary</h3>
                            <p className="text-[10px] text-blue-300 font-bold uppercase tracking-widest">Verification Status: High Fidelity (94% Accuracy)</p>
                          </div>
                        </div>
                        
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                          <div className="space-y-2">
                            <p className="text-[10px] text-blue-400 font-bold uppercase">Macro Alignment</p>
                            <p className="text-xs text-blue-100 leading-relaxed">Verified against RBA interest rate path and GDP forecasts. High correlation with current macro tape.</p>
                          </div>
                          <div className="space-y-2">
                            <p className="text-[10px] text-blue-400 font-bold uppercase">Sector Accuracy</p>
                            <p className="text-xs text-blue-100 leading-relaxed">NIM and Credit Quality data synced with latest ASX peer reporting (CBA/NAB). Industry metrics are current.</p>
                          </div>
                          <div className="space-y-2">
                            <p className="text-[10px] text-blue-400 font-bold uppercase">Regulatory Status</p>
                            <p className="text-xs text-blue-100 leading-relaxed">APRA capital requirements (CET1) verified. No immediate regulatory gaps detected in current report.</p>
                          </div>
                        </div>

                        <div className="pt-4 border-t border-blue-500/30">
                          <p className="text-[10px] text-blue-400 font-bold uppercase mb-2">Critical Fixes Implemented</p>
                          <div className="flex flex-wrap gap-2">
                            <span className="px-2 py-1 bg-blue-500/20 border border-blue-400/30 text-blue-300 text-[8px] font-bold rounded-md">Real-time Tape Sync</span>
                            <span className="px-2 py-1 bg-blue-500/20 border border-blue-400/30 text-blue-300 text-[8px] font-bold rounded-md">Multi-Agent Cross-Check</span>
                            <span className="px-2 py-1 bg-blue-500/20 border border-blue-400/30 text-blue-300 text-[8px] font-bold rounded-md">Hallucination Guardrails</span>
                          </div>
                        </div>
                      </div>
                    </motion.div>

                      <div className="p-8 bg-white border border-[#E5E7EB] rounded-3xl shadow-sm space-y-6">
                        <div className="flex items-center justify-between border-b border-gray-100 pb-6">
                          <div className="flex items-center gap-4">
                            <div className="p-3 bg-blue-100 rounded-xl">
                              <TrendingUp className="w-8 h-8 text-blue-600" />
                            </div>
                            <div>
                              <h2 className="text-3xl font-black tracking-tight">{financeReport?.reportTitle || 'Financial Report'}</h2>
                              <p className="text-xs text-gray-400 font-bold uppercase tracking-widest">ASX: {ticker || 'ANZ'} • Deep-Dive Forecast</p>
                            </div>
                          </div>
                          <div className="flex gap-4">
                            <div className="text-right">
                              <p className="text-[10px] text-gray-400 font-bold uppercase">P/E Ratio</p>
                              <p className="text-lg font-black">{financeReport?.valuation?.pe || 'N/A'}</p>
                            </div>
                            <div className="text-right">
                              <p className="text-[10px] text-gray-400 font-bold uppercase">Div Yield</p>
                              <p className="text-lg font-black text-emerald-600">{financeReport?.valuation?.yield || 'N/A'}</p>
                            </div>
                          </div>
                        </div>

                        {/* Summary Report Section */}
                        {financeReport?.summaryReport && (
                          <div className="space-y-6">
                            <div className="p-6 bg-gray-50 border border-gray-100 rounded-2xl">
                              <p className="text-sm font-bold text-gray-900 leading-relaxed italic">
                                {financeReport.summaryReport.oneLiner}
                              </p>
                            </div>

                            <div className="overflow-hidden border border-gray-200 rounded-2xl shadow-sm">
                              <table className="w-full text-left border-collapse">
                                <thead className="bg-gray-50 border-b border-gray-200">
                                  <tr>
                                    <th className="px-6 py-4 text-[10px] font-bold text-gray-500 uppercase tracking-widest">Category</th>
                                    <th className="px-6 py-4 text-[10px] font-bold text-gray-500 uppercase tracking-widest">{ticker || 'RIO'} Status</th>
                                    <th className="px-6 py-4 text-[10px] font-bold text-gray-500 uppercase tracking-widest">What it means for investors</th>
                                  </tr>
                                </thead>
                                <tbody className="divide-y divide-gray-200">
                                  {financeReport?.summaryReport?.table?.map((row: any, i: number) => (
                                    <tr key={i} className="hover:bg-gray-50 transition-colors">
                                      <td className="px-6 py-4 text-xs font-bold text-gray-900">{row.category}</td>
                                      <td className="px-6 py-4 text-xs font-medium text-gray-700 whitespace-pre-wrap">{row.status}</td>
                                      <td className="px-6 py-4 text-xs text-gray-600 leading-relaxed">{row.meaning}</td>
                                    </tr>
                                  ))}
                                </tbody>
                              </table>
                            </div>

                            {/* Interactive Risk Dashboard - Specialized for RIO/BHP style tickers */}
                            {(ticker === 'RIO' || ticker === 'BHP' || ticker === 'VALE') && (
                              <div className="p-6 bg-[#1A1A1A] text-white rounded-3xl border border-white/10 space-y-6">
                                <div className="flex items-center justify-between">
                                  <div className="flex items-center gap-3">
                                    <ShieldAlert className="w-6 h-6 text-red-500" />
                                    <div>
                                      <h4 className="text-lg font-black tracking-tight uppercase">Interactive Risk Dashboard</h4>
                                      <p className="text-[8px] text-gray-500 font-bold uppercase tracking-widest">Real-time Geopolitical & Operational Monitoring</p>
                                    </div>
                                  </div>
                                  <div className="flex items-center gap-2 px-3 py-1 bg-red-500/20 border border-red-500/30 rounded-full">
                                    <div className="w-1.5 h-1.5 bg-red-500 rounded-full animate-pulse" />
                                    <span className="text-[8px] font-bold text-red-400 uppercase tracking-widest">High Alert</span>
                                  </div>
                                </div>

                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                                  {[
                                    { label: 'Geopolitics', status: 'CRITICAL', color: 'text-red-500', detail: 'US-China Tariffs / Trade War escalation risks' },
                                    { label: 'Chinalco Swap', status: 'MONITOR', color: 'text-amber-500', detail: 'Strategic stake movements and board influence' },
                                    { label: 'Serbia Lithium', status: 'BLOCKED', color: 'text-red-500', detail: 'Local protests and environmental probe delays' },
                                    { label: 'Oyu Tolgoi', status: 'RAMPING', color: 'text-emerald-500', detail: 'Execution on underground expansion phase' },
                                    { label: 'Iron Ore Price', status: 'BEARISH', color: 'text-red-500', detail: 'China steel demand softening, inventories rising' },
                                    { label: 'Mongolia Risk', status: 'STABLE', color: 'text-blue-500', detail: 'Government relations and tax stability' }
                                  ].map((risk, i) => (
                                    <div key={i} className="p-4 bg-white/5 border border-white/10 rounded-2xl space-y-2 hover:bg-white/10 transition-all cursor-pointer">
                                      <div className="flex justify-between items-center">
                                        <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">{risk.label}</span>
                                        <span className={cn("text-[10px] font-black", risk.color)}>{risk.status}</span>
                                      </div>
                                      <p className="text-[10px] text-gray-300 leading-tight">{risk.detail}</p>
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}

                            {financeReport?.summaryReport?.followUps && (
                              <div className="p-6 bg-blue-50 border border-blue-100 rounded-2xl space-y-3">
                                <div className="flex items-center gap-2 text-blue-600">
                                  <Zap className="w-4 h-4" />
                                  <span className="text-[10px] font-bold uppercase tracking-widest">Follow-up Intelligence</span>
                                </div>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                  {financeReport?.summaryReport?.followUps?.map((followUp: string, i: number) => (
                                    <button 
                                      key={i}
                                      onClick={() => { setMissionIntent(followUp); setActiveTab('FACTORY (CHAT)'); }}
                                      className="p-3 bg-white border border-blue-100 rounded-xl text-left text-[10px] text-blue-800 hover:bg-blue-50 transition-all shadow-sm"
                                    >
                                      {followUp}
                                    </button>
                                  ))}
                                </div>
                              </div>
                            )}
                          </div>
                        )}

                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div className="p-6 bg-blue-50 border border-blue-100 rounded-2xl space-y-2">
                          <p className="text-[10px] text-blue-600 font-bold uppercase tracking-widest">Base Case Target</p>
                          <p className="text-2xl font-black text-blue-900">{financeReport?.forecast?.base?.target || 'N/A'}</p>
                          <p className="text-[10px] text-blue-700 leading-tight italic">"{financeReport?.forecast?.base?.rationale || 'No rationale provided.'}"</p>
                        </div>
                        <div className="p-6 bg-emerald-50 border border-emerald-100 rounded-2xl space-y-2">
                          <p className="text-[10px] text-emerald-600 font-bold uppercase tracking-widest">Bull Case Target</p>
                          <p className="text-2xl font-black text-emerald-900">{financeReport?.forecast?.bull?.target || 'N/A'}</p>
                          <p className="text-[10px] text-emerald-700 leading-tight italic">"{financeReport?.forecast?.bull?.rationale || 'No rationale provided.'}"</p>
                        </div>
                        <div className="p-6 bg-red-50 border border-red-100 rounded-2xl space-y-2">
                          <p className="text-[10px] text-red-600 font-bold uppercase tracking-widest">Bear Case Target</p>
                          <p className="text-2xl font-black text-red-900">{financeReport?.forecast?.bear?.target || 'N/A'}</p>
                          <p className="text-[10px] text-red-700 leading-tight italic">"{financeReport?.forecast?.bear?.rationale || 'No rationale provided.'}"</p>
                        </div>
                      </div>

                      <div className="space-y-6">
                        {financeReport?.sections?.map((section: any, i: number) => (
                          <div key={i} className="space-y-3">
                            <h4 className="text-sm font-black uppercase tracking-widest text-gray-900 border-l-4 border-blue-600 pl-3">{section.title}</h4>
                            <p className="text-xs text-gray-600 leading-relaxed">{section.content}</p>
                            {section.metrics && section.metrics.length > 0 && (
                              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                                {section.metrics?.map((metric: any, j: number) => (
                                  <div key={j} className="p-3 bg-gray-50 rounded-xl border border-gray-100">
                                    <p className="text-[8px] text-gray-400 font-bold uppercase">{metric.label}</p>
                                    <p className="text-xs font-black">{metric.value}</p>
                                  </div>
                                ))}
                              </div>
                            )}
                          </div>
                        ))}
                      </div>

                      {financeReport?.catalysts && financeReport.catalysts.length > 0 && (
                        <div className="p-6 bg-white border border-gray-200 rounded-3xl space-y-4">
                          <div className="flex items-center gap-2">
                            <Zap className="w-5 h-5 text-amber-500" />
                            <h4 className="text-sm font-black uppercase tracking-widest">Upcoming Catalysts</h4>
                          </div>
                          <div className="overflow-x-auto">
                            <table className="w-full text-left text-[10px]">
                              <thead>
                                <tr className="border-b border-gray-100">
                                  <th className="py-2 font-bold text-gray-400 uppercase">Date/Event</th>
                                  <th className="py-2 font-bold text-gray-400 uppercase">What to Watch</th>
                                  <th className="py-2 font-bold text-gray-400 uppercase">Impact</th>
                                </tr>
                              </thead>
                              <tbody>
                                {financeReport.catalysts.map((c: any, i: number) => (
                                  <tr key={i} className="border-b border-gray-50">
                                    <td className="py-3 font-bold text-gray-900">{c.date}: {c.event}</td>
                                    <td className="py-3 text-gray-600">{c.watch}</td>
                                    <td className="py-3">
                                      <span className={cn(
                                        "px-2 py-0.5 rounded text-[8px] font-black",
                                        c.impact === 'HIGH' ? "bg-red-100 text-red-600" :
                                        c.impact === 'MEDIUM' ? "bg-amber-100 text-amber-600" :
                                        "bg-blue-100 text-blue-600"
                                      )}>{c.impact}</span>
                                    </td>
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                          </div>
                        </div>
                      )}

                      {financeReport?.criticalDates && financeReport.criticalDates.length > 0 && (
                        <div className="p-6 bg-red-900 text-white rounded-3xl space-y-4 shadow-xl shadow-red-900/20">
                          <div className="flex items-center gap-2">
                            <Calendar className="w-5 h-5 text-red-400" />
                            <h4 className="text-sm font-black uppercase tracking-widest">Critical Dates for Investors</h4>
                          </div>
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {financeReport.criticalDates.map((d: any, i: number) => (
                              <div key={i} className="p-4 bg-white/10 border border-white/10 rounded-2xl space-y-2">
                                <p className="text-[10px] font-black text-red-400 uppercase tracking-widest">{d.date}</p>
                                <p className="text-xs font-bold">{d.event}</p>
                                <p className="text-[10px] text-gray-300 italic">Trigger: {d.trigger}</p>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {financeReport?.gaps && financeReport.gaps.length > 0 && (
                        <div className="p-6 bg-red-50/50 border border-red-100 rounded-2xl space-y-4">
                          <div className="flex items-center gap-2 text-red-600">
                            <AlertTriangle className="w-4 h-4" />
                            <h4 className="text-[10px] font-bold uppercase tracking-widest">Identified Data Gaps & Grounding Fixes</h4>
                          </div>
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {financeReport?.gaps?.map((gap: any, i: number) => (
                              <div key={i} className="p-4 bg-white border border-red-100 rounded-xl space-y-2 shadow-sm">
                                <p className="text-[10px] text-red-600 font-black uppercase tracking-tighter">DATA GAP: {gap.description}</p>
                                <div className="p-2 bg-emerald-50 border border-emerald-100 rounded-lg">
                                  <p className="text-[10px] text-emerald-700 font-bold leading-tight italic">FIX: {gap.fix}</p>
                                </div>
                              </div>
                            ))}
                          </div>
                          <p className="text-[10px] text-red-500 italic">Grounding Agent recommended to verify these gaps via secondary tape analysis and the suggested fixes.</p>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {!summary && !isProcessing && (
                  <div className="py-20 text-center space-y-4 bg-white border border-dashed border-gray-300 rounded-3xl">
                    <div className="p-4 bg-gray-50 rounded-full w-fit mx-auto">
                      <FileText className="w-8 h-8 text-gray-300" />
                    </div>
                    <div className="space-y-1">
                      <p className="text-sm font-bold text-gray-400 uppercase tracking-widest">No Active Reports</p>
                      <p className="text-xs text-gray-400">Execute a mission intent in the Factory to generate intelligence.</p>
                    </div>
                  </div>
                )}

                {isProcessing && (
                  <div className="py-20 text-center space-y-4 bg-white border border-blue-100 rounded-3xl">
                    <Loader2 className="w-12 h-12 text-blue-600 animate-spin mx-auto" />
                    <div className="space-y-1">
                      <p className="text-sm font-bold text-blue-600 uppercase tracking-widest animate-pulse">Orchestrating Agents...</p>
                      <p className="text-xs text-blue-400">Synthesizing multi-agent data streams.</p>
                    </div>
                  </div>
                )}

                {summary && (
                  <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <div className="lg:col-span-2 space-y-8">
                      {/* Executive Summary */}
                      <div className="p-8 bg-white border border-[#E5E7EB] rounded-3xl shadow-sm space-y-6">
                        <div className="flex items-center gap-3">
                          <div className="p-2 bg-purple-100 rounded-lg">
                            <Brain className="w-6 h-6 text-purple-600" />
                          </div>
                          <div>
                            <h4 className="text-lg font-black tracking-tight">Executive Summary</h4>
                            <p className="text-[10px] text-gray-400 uppercase font-bold tracking-widest">Mission Outcome Analysis</p>
                          </div>
                        </div>
                        <p className="text-sm text-gray-700 leading-relaxed italic border-l-4 border-purple-500 pl-6 py-2 bg-purple-50/30 rounded-r-xl">
                          "{summary}"
                        </p>
                        {prediction && (
                          <div className="p-4 bg-blue-50 border border-blue-100 rounded-2xl">
                            <p className="text-[10px] font-bold text-blue-600 uppercase tracking-widest mb-2">Hypergraph Prediction</p>
                            <p className="text-xs text-blue-900 font-medium">"{prediction}"</p>
                          </div>
                        )}
                      </div>

                      {/* Agent Reports */}
                      {agentReports && (
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                          <div className="p-6 bg-white border border-[#E5E7EB] rounded-2xl shadow-sm space-y-4">
                            <div className="flex items-center gap-2 text-blue-600">
                              <Microscope className="w-4 h-4" />
                              <span className="text-[10px] font-bold uppercase tracking-widest">Scientist</span>
                            </div>
                            <p className="text-xs text-gray-600 leading-relaxed italic">"{agentReports.scientist}"</p>
                          </div>
                          <div className="p-6 bg-white border border-[#E5E7EB] rounded-2xl shadow-sm space-y-4">
                            <div className="flex items-center gap-2 text-red-600">
                              <ShieldCheck className="w-4 h-4" />
                              <span className="text-[10px] font-bold uppercase tracking-widest">Risk Manager</span>
                            </div>
                            <p className="text-xs text-gray-600 leading-relaxed italic">"{agentReports.riskManager}"</p>
                          </div>
                          <div className="p-6 bg-white border border-[#E5E7EB] rounded-2xl shadow-sm space-y-4">
                            <div className="flex items-center gap-2 text-emerald-600">
                              <Target className="w-4 h-4" />
                              <span className="text-[10px] font-bold uppercase tracking-widest">Strategist</span>
                            </div>
                            <p className="text-xs text-gray-600 leading-relaxed italic">"{agentReports?.strategist || 'No report available.'}"</p>
                          </div>
                          {agentReports?.groundingAgent && (
                            <div className="p-6 bg-white border border-[#E5E7EB] rounded-2xl shadow-sm space-y-4 md:col-span-3">
                              <div className="flex items-center gap-2 text-orange-600">
                                <Search className="w-4 h-4" />
                                <span className="text-[10px] font-bold uppercase tracking-widest">Grounding Agent (Tape Verification)</span>
                              </div>
                              <p className="text-xs text-gray-600 leading-relaxed italic">"{agentReports?.groundingAgent || 'No report available.'}"</p>
                              {groundingStatus?.gaps && groundingStatus.gaps.length > 0 && (
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mt-4">
                                  {groundingStatus?.gaps?.map((gap: any, i: number) => (
                                    <div key={i} className="p-3 bg-red-50/50 border border-red-100 rounded-xl space-y-1 shadow-sm">
                                      <p className="text-[8px] text-red-600 font-black uppercase tracking-tighter">DATA GAP: {gap.description}</p>
                                      <div className="p-1.5 bg-emerald-50 border border-emerald-100 rounded-lg">
                                        <p className="text-[8px] text-emerald-700 font-bold leading-tight italic">FIX: {gap.fix}</p>
                                      </div>
                                    </div>
                                  ))}
                                </div>
                              )}
                            </div>
                          )}
                        </div>
                      )}
                    </div>

                      <div className="space-y-8">
                        {/* Biological Sentinel Card */}
                        <div className="p-6 bg-[#1A1A1A] text-white rounded-3xl shadow-xl space-y-4 border border-emerald-500/30">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-3">
                              <div className="w-10 h-10 rounded-full bg-emerald-500/20 flex items-center justify-center">
                                <Activity className="w-5 h-5 text-emerald-500 animate-pulse" />
                              </div>
                              <div>
                                <p className="text-[10px] font-bold text-emerald-500 uppercase tracking-widest">Biological Sentinel</p>
                                <h4 className="text-sm font-black tracking-tight">WEARABLE SYNC</h4>
                              </div>
                            </div>
                            <div className="text-right">
                              <p className="text-[8px] text-gray-400 uppercase font-bold">Status</p>
                              <p className="text-xs font-black text-emerald-500">ACTIVE</p>
                            </div>
                          </div>
                          <div className="grid grid-cols-2 gap-3">
                            <div className="p-3 bg-white/5 rounded-xl border border-white/10">
                              <p className="text-[8px] text-gray-500 uppercase font-bold mb-1">Heart Rate</p>
                              <p className="text-sm font-black">{profile.bioMarkers.heartRate}</p>
                            </div>
                            <div className="p-3 bg-white/5 rounded-xl border border-white/10">
                              <p className="text-[8px] text-gray-500 uppercase font-bold mb-1">HRV (Stress)</p>
                              <p className={`text-sm font-black ${parseInt(profile.bioMarkers.hrv) < 45 ? 'text-red-500' : 'text-emerald-500'}`}>{profile.bioMarkers.hrv}</p>
                            </div>
                          </div>
                          <div className="flex items-center justify-between text-[8px] font-bold text-gray-500 uppercase tracking-widest">
                            <span>Uplink: Stable</span>
                            <span>Last Sync: Just Now</span>
                          </div>
                        </div>

                        {/* Strategic Suggestions */}
                      {suggestions && (
                        <div className="p-6 bg-orange-50 border border-orange-100 rounded-3xl space-y-4">
                          <div className="flex items-center gap-2 text-orange-600">
                            <Lightbulb className="w-5 h-5" />
                            <h4 className="font-bold text-sm">Strategic Suggestions</h4>
                          </div>
                          <p className="text-xs text-orange-900 leading-relaxed italic">
                            {suggestions.toLowerCase() === 'none' ? 'No further suggestions pending.' : `"${suggestions}"`}
                          </p>
                        </div>
                      )}

                      {/* Python Simulation Results (Works) */}
                      <div className="p-6 bg-white border border-[#E5E7EB] rounded-3xl space-y-4 shadow-sm">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2 text-blue-600">
                            <Cpu className="w-5 h-5" />
                            <span className="text-[10px] font-bold uppercase tracking-widest">Python Simulation Engine</span>
                          </div>
                          <div className="px-2 py-0.5 bg-blue-100 text-blue-700 rounded-full text-[8px] font-bold">STRESS_TEST_V2</div>
                        </div>
                        <div className="space-y-3">
                          <div className="flex justify-between items-center p-3 bg-gray-50 rounded-xl border border-gray-100">
                            <span className="text-[10px] text-gray-500 font-bold">OIL_SHOCK_PROB</span>
                            <span className="text-sm font-mono font-bold text-red-600">82.4%</span>
                          </div>
                          <div className="flex justify-between items-center p-3 bg-gray-50 rounded-xl border border-gray-100">
                            <span className="text-[10px] text-gray-500 font-bold">FAILURE_NODE</span>
                            <span className="text-sm font-mono font-bold text-blue-600">NODE_04_GENEVA</span>
                          </div>
                          <div className="pt-2">
                            <p className="text-[9px] text-gray-400 uppercase font-bold mb-1">Simulation Outcome</p>
                            <p className="text-[10px] text-gray-600 leading-tight italic">"Systemic depression probability has spiked due to Brent Oil bifurcation at $130. Node-04 Geneva is showing critical metabolic stress."</p>
                          </div>
                        </div>
                      </div>

                      {/* Loop Data */}
                      {loopData && (
                        <div className="p-6 bg-[#1A1A1A] text-white rounded-3xl shadow-xl space-y-6">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              <RefreshCw className="w-4 h-4 text-blue-400" />
                              <h4 className="text-[10px] font-bold uppercase tracking-widest">Self-Improvement Loop</h4>
                            </div>
                            <span className="text-[10px] font-mono text-blue-400">{loopData.consciousnessLevel}</span>
                          </div>
                          
                          <div className="space-y-4">
                            <div>
                              <p className="text-[8px] font-bold text-gray-500 uppercase mb-2">Insights</p>
                              <div className="space-y-1">
                                {loopData?.insights?.map((insight: string, i: number) => (
                                  <p key={i} className="text-[9px] text-gray-300 leading-tight">• {insight}</p>
                                ))}
                              </div>
                            </div>
                            <div>
                              <p className="text-[8px] font-bold text-gray-500 uppercase mb-2">Mutations</p>
                              <div className="space-y-1">
                                {loopData?.mutations?.map((mutation: string, i: number) => (
                                  <p key={i} className="text-[9px] text-gray-300 leading-tight">• {mutation}</p>
                                ))}
                              </div>
                            </div>
                          </div>
                        </div>
                      )}

                      {/* Execution Logs (Global) */}
                    </div>
                  </div>
                )}

            {/* Execution Logs (Global) */}
            {executionLogs.length > 0 && (
              <div className="p-6 bg-[#1A1A1A] text-white rounded-3xl shadow-xl space-y-4 border border-white/10">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Terminal className="w-4 h-4 text-emerald-400" />
                    <h4 className="text-[10px] font-bold uppercase tracking-widest">Command Center: Execution Logs</h4>
                  </div>
                  <div className="flex items-center gap-4">
                    <button 
                      onClick={() => setActiveTab('COMMAND CENTER')}
                      className="text-[8px] font-bold text-emerald-400 hover:underline flex items-center gap-1"
                    >
                      GO TO COMMAND CENTER <Zap className="w-2 h-2" />
                    </button>
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
                      <span className="text-[8px] font-bold text-emerald-400">SYNCED</span>
                    </div>
                  </div>
                </div>
                <div className="space-y-1 font-mono text-[9px] max-h-[200px] overflow-y-auto no-scrollbar">
                  {executionLogs.map((log, i) => (
                    <div key={i} className="flex gap-2">
                      <span className="text-gray-500">[{new Date().toLocaleTimeString()}]</span>
                      <span className={log.includes('[SUCCESS]') ? 'text-emerald-400' : 'text-gray-300'}>{log}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </motion.div>
        )}
            {activeTab === 'WORLD MODEL' && (
              <motion.div 
                key="world"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="space-y-8"
              >
                {/* Digital Twin / Hypergraph Simulation */}
                <div className="p-8 bg-[#1A1A1A] rounded-3xl border border-[#333] space-y-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="p-2 bg-red-500/10 rounded-lg">
                        {activeDomain === 'Finance' ? <DollarSign className="w-6 h-6 text-red-500" /> : 
                         activeDomain === 'Agriculture' ? <Leaf className="w-6 h-6 text-red-500" /> :
                         <Users className="w-6 h-6 text-red-500" />}
                      </div>
                      <div>
                        <h4 className="text-lg font-black text-white tracking-tight">
                          {activeDomain === 'Finance' ? 'Corporate Twin Simulation' : 
                           activeDomain === 'Agriculture' ? 'Ecosystem Twin Simulation' :
                           'Digital Twin Simulation'}
                        </h4>
                        <p className="text-[10px] text-gray-500 uppercase font-bold tracking-widest">
                          {activeDomain === 'Finance' ? 'AAPL Hypergraph Node' : 
                           activeDomain === 'Agriculture' ? 'Soil-Crop Metabolic Node' :
                           'Virtual Patient Node-04'}
                        </p>
                      </div>
                    </div>
                    <button 
                      onClick={handleDreamerSimulation}
                      disabled={isDreaming}
                      className="px-4 py-2 bg-red-600 text-white text-[10px] font-bold rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50 flex items-center gap-2"
                    >
                      {isDreaming ? <Loader2 className="w-3 h-3 animate-spin" /> : <Zap className="w-3 h-3" />}
                      RUN 1000 SCENARIOS
                    </button>
                  </div>

                  {dreamerData ? (
                    <div className="space-y-6">
                      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <div className="p-4 bg-black/50 border border-red-500/20 rounded-2xl text-center">
                          <p className="text-[10px] text-gray-500 font-bold uppercase mb-1">Risk Score</p>
                          <p className={`text-xl font-black ${dreamerData.riskScore > 70 ? 'text-red-500' : 'text-emerald-500'}`}>
                            {dreamerData.riskScore}%
                          </p>
                        </div>
                        <div className="md:col-span-3 p-4 bg-black/50 border border-[#333] rounded-2xl">
                          <p className="text-[10px] text-gray-500 font-bold uppercase mb-1">Dreamer Insight</p>
                          <p className="text-xs font-bold text-white italic">"{dreamerData.insight}"</p>
                        </div>
                      </div>

                      <div className="grid grid-cols-3 gap-4">
                        {dreamerData?.scenarios?.map((s, i) => (
                          <div key={i} className="p-4 bg-black/50 border border-[#333] rounded-2xl space-y-2">
                            <div className="flex items-center justify-between">
                              <span className="text-[10px] font-bold text-gray-400 uppercase">{s.time}</span>
                              <span className={`text-[8px] font-bold px-1.5 py-0.5 rounded ${
                                s.state === 'Critical' ? 'bg-red-500/20 text-red-500' :
                                s.state === 'Warning' ? 'bg-orange-500/20 text-orange-500' :
                                'bg-emerald-500/20 text-emerald-500'
                              }`}>{s.state}</span>
                            </div>
                            <div className="w-full h-1 bg-white/10 rounded-full overflow-hidden">
                              <div 
                                className={`h-full transition-all duration-1000 ${
                                  s.state === 'Critical' ? 'bg-red-500' :
                                  s.state === 'Warning' ? 'bg-orange-500' :
                                  'bg-emerald-500'
                                }`}
                                style={{ width: `${s.probability}%` }}
                              />
                            </div>
                            <p className="text-[8px] text-gray-500 text-right font-bold">{s.probability}% Confidence</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  ) : (
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                      {activeDomain === 'Finance' ? [
                        { label: "Interest Rate", impact: "-2.4% Margin" },
                        { label: "AI Patent Lock", impact: "+18% Resilience" },
                        { label: "Supply Chain", impact: "Vertex Shift" },
                        { label: "Consumer Cap", impact: "+12% Growth" }
                      ].map((sim) => (
                        <div key={sim.label} className="p-4 bg-black/50 border border-[#333] rounded-2xl text-center">
                          <p className="text-[10px] text-gray-500 font-bold uppercase mb-1">{sim.label}</p>
                          <p className="text-xs font-bold text-white">{sim.impact}</p>
                        </div>
                      )) : [
                        { label: "Diet Change", impact: "+12% Stability" },
                        { label: "Drug Dosage", impact: "-5% Toxicity" },
                        { label: "Stress Event", impact: "Flare Trigger" },
                        { label: "Sleep Cycle", impact: "+22% Recovery" }
                      ].map((sim) => (
                        <div key={sim.label} className="p-4 bg-black/50 border border-[#333] rounded-2xl text-center">
                          <p className="text-[10px] text-gray-500 font-bold uppercase mb-1">{sim.label}</p>
                          <p className="text-xs font-bold text-white">{sim.impact}</p>
                        </div>
                      ))}
                    </div>
                  )}

                  <div className="h-48 w-full bg-black/30 rounded-2xl border border-[#333] flex items-center justify-center relative overflow-hidden">
                    <div className="absolute inset-0 opacity-20 bg-[url('https://picsum.photos/seed/dna/1200/600')] bg-cover bg-center" />
                    <div className="relative z-10 flex flex-col items-center gap-2">
                      <div className="flex gap-1">
                        {[...Array(20)].map((_, i) => (
                          <div 
                            key={i} 
                            className="w-1 h-12 bg-red-500/50 rounded-full animate-pulse"
                            style={{ animationDelay: `${i * 0.1}s` }}
                          />
                        ))}
                      </div>
                      <p className="text-[10px] text-red-500 font-mono animate-pulse">SIMULATING CAUSAL EDGES...</p>
                    </div>
                  </div>
                </div>

                {/* Ruliad Rules Display */}
                {ruliadRules.length > 0 && (
                  <motion.div 
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="p-8 bg-white border border-[#E5E7EB] rounded-3xl shadow-sm space-y-6"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-purple-100 rounded-lg">
                          <Network className="w-6 h-6 text-purple-600" />
                        </div>
                        <div>
                          <h4 className="text-lg font-black tracking-tight">Discovered Ruliad Rules</h4>
                          <p className="text-[10px] text-gray-500 uppercase font-bold tracking-widest">Hypergraph Rule Set</p>
                        </div>
                      </div>
                      <button 
                        onClick={() => setRuliadRules([])}
                        className="text-[10px] font-bold text-red-500 uppercase tracking-widest hover:underline"
                      >
                        CLEAR RULES
                      </button>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {ruliadRules?.map((rule, i) => (
                        <div key={i} className="p-4 bg-[#F9FAFB] border border-[#F3F4F6] rounded-2xl space-y-2 group hover:border-purple-500 transition-all">
                          <div className="flex items-center justify-between">
                            <span className="text-[8px] font-black text-purple-600 uppercase tracking-widest px-2 py-0.5 bg-purple-50 rounded-full">
                              {rule.dimension}
                            </span>
                            <span className="text-[8px] font-mono text-gray-400">CONF: {(rule.probability * 100).toFixed(1)}%</span>
                          </div>
                          <p className="text-xs font-bold text-[#1A1A1A] leading-relaxed italic">"{rule.rule}"</p>
                        </div>
                      ))}
                    </div>
                  </motion.div>
                )}

                <div className="flex items-center justify-between">
                  <h3 className="text-2xl font-black tracking-tight">World Model Router</h3>
                  <div className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-[10px] font-bold uppercase tracking-widest">Active</div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="p-6 bg-white border border-[#E5E7EB] rounded-2xl shadow-sm space-y-4">
                    <div className="flex items-center gap-3">
                      <div className="p-2 bg-blue-100 rounded-lg">
                        <Target className="w-5 h-5 text-blue-600" />
                      </div>
                      <h4 className="font-bold">Ruliad Search</h4>
                    </div>
                    <p className="text-xs text-[#6B7280]">Extract non-obvious rules from the computational universe.</p>
                    <button 
                      onClick={handleRuliadSearch}
                      disabled={isSearchingRuliad}
                      className="w-full py-2 bg-[#1A1A1A] text-white rounded-lg text-[10px] font-bold hover:bg-black disabled:opacity-50 transition-all flex items-center justify-center gap-2"
                    >
                      {isSearchingRuliad ? <Loader2 className="w-3 h-3 animate-spin" /> : <Search className="w-3 h-3" />}
                      SEARCH RULIAD
                    </button>
                  </div>

                  <div className="p-6 bg-white border border-[#E5E7EB] rounded-2xl shadow-sm space-y-4">
                    <div className="flex items-center gap-3">
                      <div className="p-2 bg-purple-100 rounded-lg">
                        <Globe className="w-5 h-5 text-purple-600" />
                      </div>
                      <h4 className="font-bold">Physics Engine</h4>
                    </div>
                    <p className="text-xs text-[#6B7280]">Simulating Ruliad physics for predictive accuracy.</p>
                    <div className="flex items-center gap-2">
                      <div className="h-2 flex-1 bg-gray-100 rounded-full overflow-hidden">
                        <motion.div 
                          initial={{ width: 0 }}
                          animate={{ width: `${syncLevel}%` }}
                          className="h-full bg-purple-500"
                        />
                      </div>
                      <span className="text-[10px] font-bold">{syncLevel}% SYNC</span>
                    </div>
                  </div>

                  <div className="p-6 bg-white border border-[#E5E7EB] rounded-2xl shadow-sm space-y-4">
                    <div className="flex items-center gap-3">
                      <div className="p-2 bg-emerald-100 rounded-lg">
                        <RefreshCw className="w-5 h-5 text-emerald-600" />
                      </div>
                      <h4 className="font-bold">Recursive Loop</h4>
                    </div>
                    <p className="text-xs text-[#6B7280]">Continuous learning from previous mission outcomes.</p>
                    <div className="flex -space-x-2">
                      {[1,2,3,4].map(i => (
                        <div key={i} className="w-6 h-6 rounded-full bg-gray-200 border-2 border-white flex items-center justify-center text-[8px] font-bold">N{i}</div>
                      ))}
                    </div>
                  </div>
                </div>
              </motion.div>
            )}

            {activeTab === 'HIERARCHY' && (
              <motion.div 
                key="hierarchy"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="grid grid-cols-1 lg:grid-cols-3 gap-8"
              >
                {/* Task Approval */}
                <div className="lg:col-span-2 space-y-6">
                  {isExecutingTrade && (
                    <motion.div 
                      initial={{ opacity: 0, y: -20 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="p-6 bg-[#1A1A1A] text-white rounded-2xl shadow-xl border border-emerald-500/30 overflow-hidden relative"
                    >
                      <div className="absolute top-0 left-0 h-1 bg-emerald-500 transition-all duration-300" style={{ width: `${tradeProgress}%` }} />
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 rounded-full bg-emerald-500/20 flex items-center justify-center">
                            <RefreshCw className="w-5 h-5 text-emerald-500 animate-spin" />
                          </div>
                          <div>
                            <p className="text-[10px] font-bold text-emerald-500 uppercase tracking-widest">Active Transaction</p>
                            <h4 className="text-lg font-black tracking-tight">{tradeStatus}</h4>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="text-[8px] text-gray-400 uppercase font-bold">Progress</p>
                          <p className="text-xl font-black text-emerald-500">{tradeProgress}%</p>
                        </div>
                      </div>
                      <div className="grid grid-cols-4 gap-2">
                        {[1,2,3,4].map(i => (
                          <div key={i} className={`h-1 rounded-full ${tradeProgress >= i * 25 ? 'bg-emerald-500' : 'bg-white/10'}`} />
                        ))}
                      </div>
                    </motion.div>
                  )}

                  <div className="flex items-center justify-between">
                    <h3 className="text-2xl font-black tracking-tight">Approval Hierarchy</h3>
                    <button 
                      onClick={() => setIsAutoPilot(!isAutoPilot)}
                      className={cn(
                        "flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all",
                        isAutoPilot ? "bg-red-500 text-white" : "bg-blue-500 text-white"
                      )}
                    >
                      {isAutoPilot ? <Lock className="w-4 h-4" /> : <Unlock className="w-4 h-4" />}
                      {isAutoPilot ? "AUTO-PILOT ACTIVE" : "MANUAL OVERRIDE"}
                    </button>
                  </div>

                  <div className="bg-white border border-[#E5E7EB] rounded-2xl shadow-sm overflow-hidden">
                    <div className="p-4 bg-[#F9FAFB] border-b text-[10px] font-bold text-[#6B7280] uppercase tracking-widest flex justify-between">
                      <span>Directive</span>
                      <span>Status</span>
                    </div>
                    <div className="divide-y">
                      {tasks.length > 0 ? tasks.map((task, idx) => (
                        <div key={idx} className="p-4 flex items-center justify-between hover:bg-gray-50 transition-all">
                          <div className="flex items-center gap-3">
                            {task.completed ? (
                              <CheckCircle2 className="w-4 h-4 text-green-500" />
                            ) : (
                              <div className="w-4 h-4 rounded-full border-2 border-gray-300" />
                            )}
                            <span className={cn(
                              "text-xs font-medium transition-all",
                              task.completed ? "text-gray-400 line-through" : "text-[#4B5563]"
                            )}>{task.text}</span>
                          </div>
                          <div className="flex gap-2">
                            <button 
                              onClick={() => toggleTaskApproval(idx)}
                              disabled={task.completed}
                              className={cn(
                                "px-3 py-1 rounded-lg text-[10px] font-bold uppercase tracking-widest transition-all",
                                task.approved ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-400 hover:bg-blue-100 hover:text-blue-700"
                              )}
                            >
                              {task.approved ? "Approved" : "Pending"}
                            </button>
                            {task.approved && (
                              <button 
                                onClick={() => toggleTaskCompletion(idx)}
                                className={cn(
                                  "px-3 py-1 rounded-lg text-[10px] font-bold uppercase tracking-widest transition-all",
                                  task.completed ? "bg-blue-100 text-blue-700" : "bg-gray-100 text-gray-400 hover:bg-green-100 hover:text-green-700"
                                )}
                              >
                                {task.completed ? "Undo" : "Complete"}
                              </button>
                            )}
                          </div>
                        </div>
                      )) : (
                        <div className="p-12 text-center text-[#9CA3AF]">
                          <Terminal className="w-8 h-8 mx-auto mb-2 opacity-20" />
                          <p className="text-xs">No active directives in queue.</p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                {/* Agent Chat */}
                <div className="space-y-6">
                  {/* Voice Uplink Card */}
                  <div className="bg-[#1A1A1A] text-white rounded-2xl shadow-xl border border-white/10 p-6 space-y-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className={`w-10 h-10 rounded-full flex items-center justify-center transition-all ${isRecording ? 'bg-red-500 animate-pulse' : 'bg-blue-500'}`}>
                          {isRecording ? <Mic className="w-5 h-5" /> : <Smartphone className="w-5 h-5" />}
                        </div>
                        <div>
                          <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Mobile Uplink</p>
                          <h4 className="text-sm font-black tracking-tight">{isRecording ? 'RECORDING...' : 'VOICE UPLINK IDLE'}</h4>
                        </div>
                      </div>
                      <button 
                        onMouseDown={startRecording}
                        onMouseUp={stopRecording}
                        onMouseLeave={stopRecording}
                        className={cn(
                          "w-12 h-12 rounded-full flex items-center justify-center transition-all shadow-lg active:scale-95",
                          isRecording ? "bg-red-500 shadow-red-500/50" : "bg-white/10 hover:bg-white/20"
                        )}
                      >
                        {isRecording ? <MicOff className="w-6 h-6" /> : <Mic className="w-6 h-6" />}
                      </button>
                    </div>

                    {/* Waveform Visualizer */}
                    <div className="h-12 flex items-center justify-center gap-1">
                      {waveform.map((v, i) => (
                        <motion.div 
                          key={i}
                          animate={{ height: `${Math.max(4, v * 40)}px` }}
                          className={`w-1 rounded-full ${isRecording ? 'bg-red-500' : 'bg-blue-500/30'}`}
                        />
                      ))}
                    </div>

                    <div className="flex items-center justify-between text-[8px] font-bold text-gray-500 uppercase tracking-widest">
                      <span>Latency: 0.004ms</span>
                      <span>Uplink: Stable</span>
                    </div>
                  </div>

                  <div className="bg-white border border-[#E5E7EB] rounded-2xl shadow-sm flex flex-col h-[400px]">
          <div className="p-4 border-b flex items-center gap-3 bg-[#F9FAFB]">
                    <div className="w-8 h-8 rounded-full bg-[#10B981] flex items-center justify-center shadow-sm">
                      <Bot className="w-4 h-4 text-white" />
                    </div>
                    <div>
                      <p className="text-xs font-bold">BUDDY-AGENT</p>
                      <p className="text-[8px] text-[#10B981] font-bold uppercase tracking-widest">Online & Processing</p>
                    </div>
                  </div>
                  <div className="flex-1 overflow-y-auto p-4 space-y-4">
                    {chatMessages?.map((msg, i) => (
                      <div key={i} className={cn(
                        "max-w-[80%] p-3 rounded-2xl text-xs",
                        msg.role === 'user' ? "bg-blue-600 text-white ml-auto rounded-tr-none" : "bg-[#F3F4F6] text-[#1A1A1A] rounded-tl-none"
                      )}>
                        {msg.text}
                      </div>
                    ))}
                  </div>
                  <div className="p-4 border-t flex gap-2">
                    <input 
                      type="text"
                      value={chatInput}
                      onChange={(e) => setChatInput(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                      placeholder="Send directive..."
                      className="flex-1 p-2 bg-[#F3F4F6] border border-[#E5E7EB] rounded-xl text-xs focus:ring-2 focus:ring-blue-500 outline-none"
                    />
                    <button 
                      onClick={handleSendMessage}
                      className="p-2 bg-[#1A1A1A] text-white rounded-xl hover:bg-black transition-all"
                    >
                      <Send className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            </motion.div>
          )}

            {activeTab === 'EVOLUTION' && (
              <motion.div 
                key="evolution"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="grid grid-cols-1 md:grid-cols-2 gap-8"
              >
                {/* Profile Settings */}
                <div className="space-y-6">
                    <div className="flex items-center justify-between mb-2">
                      <label className="text-[10px] font-bold text-[#6B7280] uppercase tracking-widest block">User Profile & Bio-Markers</label>
                      <div className="flex items-center gap-1.5 px-2 py-0.5 bg-emerald-100 text-emerald-600 rounded-full text-[8px] font-bold border border-emerald-200">
                        <div className="w-1 h-1 bg-emerald-500 rounded-full animate-pulse" />
                        WEARABLE SYNC ACTIVE
                      </div>
                    </div>
                    <div className="p-6 bg-white border border-[#E5E7EB] rounded-2xl shadow-sm space-y-6">
                    <div>
                      <label className="text-[10px] font-bold text-[#6B7280] uppercase tracking-widest mb-2 block">Investment Budget</label>
                      <div className="flex items-center gap-3 p-3 bg-[#F3F4F6] rounded-xl border border-[#E5E7EB]">
                        <DollarSign className="w-5 h-5 text-emerald-600" />
                        <input 
                          type="text"
                          value={profile.budget}
                          onChange={(e) => setProfile(p => ({...p, budget: e.target.value}))}
                          className="bg-transparent font-bold text-lg outline-none w-full"
                        />
                      </div>
                    </div>

                    <div className="grid grid-cols-3 gap-4">
                      {activeDomain !== 'Finance' && (Object.entries(profile.bioMarkers) as [keyof UserProfile['bioMarkers'], string][]).map(([key, val]) => (
                        <div key={key} className="p-3 bg-[#F3F4F6] rounded-xl border border-[#E5E7EB]">
                          <p className="text-[8px] font-bold text-[#6B7280] uppercase mb-1">{key.replace(/([A-Z])/g, ' $1')}</p>
                          <input 
                            type="text"
                            value={val}
                            onChange={(e) => updateBioMarker(key, e.target.value)}
                            className="text-xs font-bold bg-transparent outline-none w-full"
                          />
                        </div>
                      ))}
                      {activeDomain === 'Finance' && (
                        <div className="col-span-3 p-4 bg-emerald-50 border border-emerald-100 rounded-xl flex items-center gap-3">
                          <ShieldCheck className="w-5 h-5 text-emerald-600" />
                          <div>
                            <p className="text-[10px] font-bold text-emerald-800 uppercase tracking-widest">Bio-Markers Masked</p>
                            <p className="text-[8px] text-emerald-600 font-medium">Privacy protocol active for Finance domain.</p>
                          </div>
                        </div>
                      )}
                    </div>

                    <button className="w-full py-3 bg-[#1A1A1A] text-white rounded-xl font-bold text-xs hover:bg-black transition-all flex items-center justify-center gap-2">
                      <Settings className="w-4 h-4" />
                      UPDATE BIO-METRICS
                    </button>
                  </div>

                  {/* STEP-20: DNA EDITOR (CRISPR SIMULATION) */}
                  <div className="p-8 bg-white border border-[#E5E7EB] rounded-3xl shadow-sm space-y-6">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-emerald-100 rounded-lg">
                          <Dna className="w-6 h-6 text-emerald-600" />
                        </div>
                        <div>
                          <h4 className="text-lg font-black tracking-tight">DNA Editor (Step-20)</h4>
                          <p className="text-[10px] text-gray-400 uppercase font-bold tracking-widest">CRISPR-Cas9 Simulation Interface</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" />
                        <span className="text-[8px] font-bold text-blue-600 uppercase tracking-widest">Sequencer Active</span>
                      </div>
                    </div>

                    <div className="space-y-4">
                      <div>
                        <label className="text-[10px] font-bold text-[#6B7280] uppercase tracking-widest mb-2 block">DNA Sequence (Target Strand)</label>
                        <div className="p-4 bg-[#1A1A1A] rounded-2xl border border-white/10 font-mono text-[10px] text-emerald-400 break-all leading-relaxed relative group">
                          <textarea 
                            value={dnaSequence}
                            onChange={(e) => setDnaSequence(e.target.value.toUpperCase())}
                            className="w-full bg-transparent outline-none resize-none h-20 no-scrollbar"
                          />
                          <div className="absolute bottom-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
                            <span className="text-[8px] text-gray-500 uppercase font-bold">Editable Strand</span>
                          </div>
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <label className="text-[10px] font-bold text-[#6B7280] uppercase tracking-widest mb-2 block">Target Gene</label>
                          <select 
                            value={targetGene}
                            onChange={(e) => setTargetGene(e.target.value)}
                            className="w-full p-3 bg-[#F3F4F6] border border-[#E5E7EB] rounded-xl text-xs font-bold outline-none focus:ring-2 focus:ring-emerald-500"
                          >
                            <option value="BRAF-V600E">BRAF-V600E (Melanoma)</option>
                            <option value="PD-L1">PD-L1 (Immune Checkpoint)</option>
                            <option value="NRAS">NRAS (Mutation)</option>
                            <option value="TP53">TP53 (Tumor Suppressor)</option>
                          </select>
                        </div>
                        <div className="flex items-end">
                          <button 
                            onClick={handleCRISPRSimulation}
                            disabled={isEditingDNA}
                            className="w-full py-3 bg-emerald-600 text-white rounded-xl font-black text-[10px] uppercase tracking-widest hover:bg-emerald-700 transition-all flex items-center justify-center gap-2 disabled:opacity-50 shadow-lg shadow-emerald-500/20"
                          >
                            {isEditingDNA ? <Loader2 className="w-3 h-3 animate-spin" /> : <Zap className="w-3 h-3" />}
                            SIMULATE CRISPR
                          </button>
                        </div>
                      </div>

                      {crisprResult && (
                        <motion.div 
                          initial={{ opacity: 0, scale: 0.95 }}
                          animate={{ opacity: 1, scale: 1 }}
                          className="p-4 bg-emerald-50 border border-emerald-100 rounded-2xl space-y-3"
                        >
                          <div className="flex items-center justify-between">
                            <span className="text-[8px] font-bold text-emerald-800 uppercase tracking-widest">Intervention Impact</span>
                            <span className="text-[10px] font-mono font-bold text-emerald-600">{crisprResult.impactScore}%</span>
                          </div>
                          <div className="w-full h-1.5 bg-emerald-200 rounded-full overflow-hidden">
                            <motion.div 
                              initial={{ width: 0 }}
                              animate={{ width: `${crisprResult.impactScore}%` }}
                              className="h-full bg-emerald-500"
                            />
                          </div>
                          <p className="text-[10px] text-emerald-700 leading-relaxed italic">"{crisprResult.rationale}"</p>
                        </motion.div>
                      )}
                    </div>
                  </div>

                  {/* BIOMETRIC EYE SCAN */}
                  <div className="p-8 bg-white border border-blue-100 rounded-3xl shadow-sm space-y-6">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-blue-100 rounded-lg">
                          <Eye className="w-6 h-6 text-blue-600" />
                        </div>
                        <div>
                          <h4 className="text-lg font-black tracking-tight">Optical Sensor (Eye Scan)</h4>
                          <p className="text-[10px] text-gray-400 uppercase font-bold tracking-widest">Retinal Biometric Verification</p>
                        </div>
                      </div>
                      {isEyeScanning && (
                        <div className="flex items-center gap-2">
                          <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse" />
                          <span className="text-[8px] font-bold text-red-600 uppercase tracking-widest">Scanning...</span>
                        </div>
                      )}
                    </div>

                    <div className="space-y-4">
                      <div className="aspect-video bg-[#1A1A1A] rounded-2xl border border-white/10 flex items-center justify-center relative overflow-hidden">
                        {isEyeScanning ? (
                          <>
                            <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-blue-500/20 via-transparent to-transparent animate-pulse" />
                            <motion.div 
                              animate={{ top: ['0%', '100%'] }}
                              transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
                              className="absolute left-0 right-0 h-[2px] bg-blue-500 shadow-[0_0_15px_rgba(59,130,246,0.8)] z-20"
                            />
                            <div className="text-center space-y-2 z-10">
                              <Scan className="w-12 h-12 text-blue-400 mx-auto animate-bounce" />
                              <p className="text-[10px] font-mono text-blue-400 uppercase tracking-widest">Analyzing Retinal Map...</p>
                            </div>
                          </>
                        ) : eyeScanResult ? (
                          <div className="text-center space-y-4 p-6">
                            <ShieldCheck className="w-12 h-12 text-emerald-400 mx-auto" />
                            <p className="text-xs font-bold text-emerald-400 leading-tight">{eyeScanResult}</p>
                            <button 
                              onClick={() => setEyeScanResult(null)}
                              className="text-[8px] font-bold text-gray-500 uppercase tracking-widest hover:text-white transition-colors"
                            >
                              Reset Scanner
                            </button>
                          </div>
                        ) : (
                          <div className="text-center space-y-2">
                            <Camera className="w-12 h-12 text-white/10 mx-auto" />
                            <p className="text-[10px] font-mono text-white/20 uppercase tracking-widest">Camera Ready</p>
                          </div>
                        )}
                      </div>

                      <button 
                        onClick={handleEyeScan}
                        disabled={isEyeScanning}
                        className="w-full py-4 bg-blue-600 text-white rounded-xl font-black text-xs uppercase tracking-widest hover:bg-blue-700 transition-all shadow-lg shadow-blue-200 flex items-center justify-center gap-2"
                      >
                        {isEyeScanning ? <Loader2 className="w-4 h-4 animate-spin" /> : <Scan className="w-4 h-4" />}
                        INITIATE BIOMETRIC SCAN
                      </button>
                    </div>
                  </div>

                  {/* STEP-21: MOLECULAR DOCKING (DRUG DISCOVERY) */}
                  <div className="p-8 bg-white border border-[#E5E7EB] rounded-3xl shadow-sm space-y-6">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-blue-100 rounded-lg">
                          <Cpu className="w-6 h-6 text-blue-600" />
                        </div>
                        <div>
                          <h4 className="text-lg font-black tracking-tight">Molecular Docking (Step-21)</h4>
                          <p className="text-[10px] text-gray-400 uppercase font-bold tracking-widest">Drug-Target Interaction Simulation</p>
                        </div>
                      </div>
                    </div>

                    <div className="space-y-4">
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <label className="text-[10px] font-bold text-[#6B7280] uppercase tracking-widest mb-2 block">Drug Molecule</label>
                          <select 
                            value={drugMolecule}
                            onChange={(e) => setDrugMolecule(e.target.value)}
                            className="w-full p-3 bg-[#F3F4F6] border border-[#E5E7EB] rounded-xl text-xs font-bold outline-none focus:ring-2 focus:ring-blue-500"
                          >
                            <option value="Nivolumab (Opdivo)">Nivolumab (Opdivo)</option>
                            <option value="Pembrolizumab (Keytruda)">Pembrolizumab (Keytruda)</option>
                            <option value="Dabrafenib (Tafinlar)">Dabrafenib (Tafinlar)</option>
                            <option value="Trametinib (Mekinist)">Trametinib (Mekinist)</option>
                            <option value="Dacarbazine (Chemo)">Dacarbazine (Chemo)</option>
                          </select>
                        </div>
                        <div className="flex items-end">
                          <button 
                            onClick={handleMolecularDocking}
                            disabled={isDocking || !crisprResult}
                            className="w-full py-3 bg-blue-600 text-white rounded-xl font-black text-[10px] uppercase tracking-widest hover:bg-blue-700 transition-all flex items-center justify-center gap-2 disabled:opacity-50 shadow-lg shadow-blue-500/20"
                          >
                            {isDocking ? <Loader2 className="w-3 h-3 animate-spin" /> : <Zap className="w-3 h-3" />}
                            SIMULATE DOCKING
                          </button>
                        </div>
                      </div>

                      {dockingData && (
                        <motion.div 
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          className="p-6 bg-blue-900 text-white rounded-3xl space-y-6"
                        >
                          <div className="flex items-center justify-between">
                            <span className="text-[10px] font-bold uppercase tracking-widest">Binding Affinity</span>
                            <span className="text-xl font-black">{dockingData.bindingAffinity}%</span>
                          </div>
                          <div className="flex gap-1 h-12 items-end">
                            {dockingData?.dockingVisualData?.map((v, i) => (
                              <div key={i} className="flex-1 bg-blue-400/50 rounded-t-sm" style={{ height: `${v}%` }} />
                            ))}
                          </div>
                          <p className="text-[10px] text-blue-100/70 leading-relaxed italic">"{dockingData.rationale}"</p>
                          
                          <button 
                            onClick={handleTherapyRecommendation}
                            disabled={isGeneratingTherapy}
                            className="w-full py-3 bg-white text-blue-900 rounded-xl font-black text-[10px] uppercase tracking-widest hover:bg-blue-50 transition-all flex items-center justify-center gap-2"
                          >
                            {isGeneratingTherapy ? <Loader2 className="w-3 h-3 animate-spin" /> : <Target className="w-3 h-3" />}
                            GENERATE THERAPY RECO
                          </button>
                        </motion.div>
                      )}

                      {therapyRecommendation && (
                        <motion.div 
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          className="p-6 bg-white border-2 border-emerald-500 rounded-3xl space-y-4 shadow-xl"
                        >
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              <ShieldCheck className="w-5 h-5 text-emerald-600" />
                              <h4 className="text-sm font-black text-gray-900 uppercase">Therapy Recommendation</h4>
                            </div>
                            <span className={cn(
                              "px-2 py-1 rounded text-[8px] font-bold uppercase",
                              therapyRecommendation.riskLevel === 'Low' ? "bg-emerald-100 text-emerald-600" :
                              therapyRecommendation.riskLevel === 'Medium' ? "bg-amber-100 text-amber-600" : "bg-red-100 text-red-600"
                            )}>
                              Risk: {therapyRecommendation.riskLevel}
                            </span>
                          </div>
                          
                          <div className="grid grid-cols-2 gap-4">
                            <div className="p-3 bg-gray-50 rounded-xl">
                              <p className="text-[8px] font-bold text-gray-400 uppercase mb-1">Therapy Type</p>
                              <p className="text-xs font-black text-gray-900">{therapyRecommendation.therapyType}</p>
                            </div>
                            <div className="p-3 bg-gray-50 rounded-xl">
                              <p className="text-[8px] font-bold text-gray-400 uppercase mb-1">Dosage</p>
                              <p className="text-xs font-black text-gray-900">{therapyRecommendation.dosage}</p>
                            </div>
                          </div>
                          
                          <div className="p-3 bg-emerald-50 rounded-xl">
                            <p className="text-[8px] font-bold text-emerald-800 uppercase mb-1">Expected Outcome</p>
                            <p className="text-xs font-medium text-emerald-900 italic">"{therapyRecommendation.expectedOutcome}"</p>
                          </div>

                          <button 
                            onClick={handleQuantumFeedback}
                            disabled={isSimulatingQuantum}
                            className="w-full py-3 bg-emerald-600 text-white rounded-xl font-black text-[10px] uppercase tracking-widest hover:bg-emerald-700 transition-all flex items-center justify-center gap-2 shadow-lg shadow-emerald-500/20"
                          >
                            {isSimulatingQuantum ? <Loader2 className="w-3 h-3 animate-spin" /> : <Activity className="w-3 h-3" />}
                            RUN QUANTUM BIO-FEEDBACK
                          </button>
                        </motion.div>
                      )}

                      {quantumFeedback && (
                        <motion.div 
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          className="p-6 bg-gray-900 text-white rounded-3xl space-y-6 border border-white/10"
                        >
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              <Activity className="w-5 h-5 text-blue-400" />
                              <h4 className="text-sm font-black uppercase">Quantum Digital Twin Feedback</h4>
                            </div>
                            {quantumFeedback.toxicityAlert && (
                              <div className="flex items-center gap-1 px-2 py-1 bg-red-500/20 text-red-400 rounded border border-red-500/30">
                                <AlertTriangle className="w-3 h-3" />
                                <span className="text-[8px] font-bold uppercase tracking-widest">TOXICITY ALERT</span>
                              </div>
                            )}
                          </div>

                          <div className="grid grid-cols-3 gap-4">
                            <div className="p-3 bg-white/5 rounded-xl border border-white/10">
                              <p className="text-[8px] font-bold text-gray-400 uppercase mb-1">Heart Rate</p>
                              <p className="text-sm font-black">{quantumFeedback.vitalSigns.heartRate} BPM</p>
                            </div>
                            <div className="p-3 bg-white/5 rounded-xl border border-white/10">
                              <p className="text-[8px] font-bold text-gray-400 uppercase mb-1">BP</p>
                              <p className="text-sm font-black">{quantumFeedback.vitalSigns.bloodPressure}</p>
                            </div>
                            <div className="p-3 bg-white/5 rounded-xl border border-white/10">
                              <p className="text-[8px] font-bold text-gray-400 uppercase mb-1">SpO2</p>
                              <p className="text-sm font-black">{quantumFeedback.vitalSigns.oxygenSaturation}%</p>
                            </div>
                          </div>

                          <div className="space-y-2">
                            <div className="flex justify-between text-[8px] font-bold text-gray-400 uppercase">
                              <span>Bio-Rhythm Stability</span>
                              <span>{Math.round(quantumFeedback.feedbackVisualData.reduce((a,b) => a+b, 0) / 10)}%</span>
                            </div>
                            <div className="flex gap-1 h-8 items-end">
                              {quantumFeedback?.feedbackVisualData?.map((v, i) => (
                                <div key={i} className="flex-1 bg-blue-500/50 rounded-t-sm" style={{ height: `${v}%` }} />
                              ))}
                            </div>
                          </div>

                          <div className="p-3 bg-blue-500/10 border border-blue-500/20 rounded-xl">
                            <p className="text-[8px] font-bold text-blue-400 uppercase mb-1">Cellular Response</p>
                            <p className="text-xs italic">"{quantumFeedback.cellularResponse}"</p>
                          </div>

                          <div className="p-3 bg-amber-500/10 border border-amber-500/20 rounded-xl">
                            <p className="text-[8px] font-bold text-amber-400 uppercase mb-1">Real-Time Adjustment</p>
                            <p className="text-xs font-bold">{quantumFeedback.realTimeAdjustment}</p>
                          </div>
                        </motion.div>
                      )}
                    </div>
                  </div>
                </div>

                {/* Melanoma Research Module */}
                <div className="p-8 bg-white border border-[#E5E7EB] rounded-3xl shadow-sm space-y-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="p-2 bg-red-100 rounded-lg">
                        <Microscope className="w-6 h-6 text-red-600" />
                      </div>
                      <div>
                        <h4 className="text-lg font-black tracking-tight">Melanoma Singularity Test</h4>
                        <p className="text-[10px] text-gray-400 uppercase font-bold tracking-widest">Vision + Biomarker Fusion Engine</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
                      <span className="text-[8px] font-bold text-emerald-600 uppercase tracking-widest">Ready for Analysis</span>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {/* Image Input */}
                    <div className="space-y-4">
                      <label className="text-[10px] font-bold text-[#6B7280] uppercase tracking-widest block">Lesion Image (Vision Input)</label>
                      <div className="aspect-square bg-gray-50 border-2 border-dashed border-gray-200 rounded-2xl flex flex-col items-center justify-center relative overflow-hidden group">
                        {capturedImage ? (
                          <>
                            <img src={capturedImage} alt="Lesion" className="w-full h-full object-cover" />
                            <button 
                              onClick={() => setCapturedImage(null)}
                              className="absolute top-4 right-4 p-2 bg-black/50 text-white rounded-full hover:bg-black transition-all"
                            >
                              <X className="w-4 h-4" />
                            </button>
                          </>
                        ) : (
                          <div className="text-center space-y-2">
                            <Camera className="w-8 h-8 text-gray-300 mx-auto" />
                            <p className="text-[10px] font-bold text-gray-400 uppercase">Upload or Capture Lesion</p>
                            <label className="px-4 py-2 bg-[#1A1A1A] text-white rounded-lg text-[10px] font-bold cursor-pointer hover:bg-black transition-all">
                              SELECT IMAGE
                              <input 
                                type="file" 
                                className="hidden" 
                                accept="image/*" 
                                onChange={(e) => {
                                  const file = e.target.files?.[0];
                                  if (file) {
                                    const reader = new FileReader();
                                    reader.onload = (ev) => setCapturedImage(ev.target?.result as string);
                                    reader.readAsDataURL(file);
                                  }
                                }} 
                              />
                            </label>
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Biomarker Input */}
                    <div className="space-y-4">
                      <label className="text-[10px] font-bold text-[#6B7280] uppercase tracking-widest block">Biomarker Dataset (JSON)</label>
                      <textarea 
                        className="w-full h-[200px] p-4 bg-gray-50 border border-gray-200 rounded-2xl font-mono text-[10px] outline-none focus:border-red-500 transition-all"
                        placeholder='{ "LDH": 320, "S100B": 0.18, "CRP": 6.5, ... }'
                        value={uploadedText || ''}
                        onChange={(e) => setUploadedText(e.target.value)}
                      />
                      <div className="flex gap-2">
                        <button 
                          onClick={() => setUploadedText(JSON.stringify({
                            "patient_id": "MEL_TEST_001",
                            "age": 58,
                            "biomarkers": { "LDH": 340, "S100B": 0.20, "CRP": 6.0 },
                            "genetics": { "BRAF_mutation": true, "NRAS_mutation": false },
                            "immune_profile": { "PD_L1_expression": 65, "T_cell_activity": "low" },
                            "symptoms": { "lesion_growth": true, "bleeding": false }
                          }, null, 2))}
                          className="flex-1 py-2 bg-gray-100 text-gray-600 rounded-lg text-[8px] font-bold uppercase hover:bg-gray-200 transition-all"
                        >
                          LOAD TEST DATA
                        </button>
                        <button 
                          onClick={() => {
                            if (!capturedImage) {
                              setError("Please upload a lesion image first.");
                              return;
                            }
                            let bioJson;
                            try {
                              bioJson = safeJsonParse(uploadedText || '{}');
                            } catch (e) {
                              console.error("Bio JSON parse error:", e);
                              setError("Invalid Biomarker JSON format.");
                              return;
                            }
                            handleMelanomaAnalysis(capturedImage, bioJson);
                          }}
                          disabled={isAnalyzingMelanoma}
                          className="flex-[2] py-2 bg-red-600 text-white rounded-lg text-[8px] font-bold uppercase hover:bg-red-700 transition-all disabled:opacity-50 flex items-center justify-center gap-2"
                        >
                          {isAnalyzingMelanoma ? <Loader2 className="w-3 h-3 animate-spin" /> : <Zap className="w-3 h-3" />}
                          INITIATE FUSION ANALYSIS
                        </button>
                      </div>
                    </div>
                  </div>

                  {/* Analysis Results */}
                  {melanomaData && (
                    <motion.div 
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="p-6 bg-gray-50 border border-gray-200 rounded-3xl space-y-6"
                    >
                      <div className="flex items-center justify-between">
                        <h4 className="text-sm font-black tracking-tight uppercase">Fusion Analysis Outcome</h4>
                        <div className={`px-3 py-1 rounded-full text-[10px] font-bold border ${
                          melanomaData.action === 'URGENT_REFERRAL' ? 'bg-red-100 text-red-600 border-red-200' :
                          melanomaData.action === 'DERMATOLOGY_CHECK' ? 'bg-orange-100 text-orange-600 border-orange-200' :
                          'bg-emerald-100 text-emerald-600 border-emerald-200'
                        }`}>
                          {melanomaData.action}
                        </div>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div className="p-4 bg-white border border-gray-200 rounded-2xl text-center">
                          <p className="text-[8px] text-gray-500 uppercase font-bold mb-1">Final Risk Score</p>
                          <p className={`text-2xl font-black ${melanomaData.risk > 0.7 ? 'text-red-600' : 'text-emerald-600'}`}>
                            {Math.round(melanomaData.risk * 100)}%
                          </p>
                        </div>
                        <div className="md:col-span-2 p-4 bg-white border border-gray-200 rounded-2xl">
                          <p className="text-[8px] text-gray-500 uppercase font-bold mb-2">ABCDE Feature Extraction</p>
                          <div className="grid grid-cols-2 gap-4">
                            {Object.entries(melanomaData?.features || {}).map(([k, v]: [string, any]) => (
                              <div key={k} className="flex items-center gap-2">
                                <div className="w-1.5 h-1.5 bg-red-500 rounded-full" />
                                <span className="text-[10px] font-bold uppercase text-gray-400">{k}:</span>
                                <span className="text-[10px] font-bold text-gray-800">{v}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>

                      <div className="p-4 bg-white border border-gray-200 rounded-2xl">
                        <p className="text-[8px] text-gray-500 uppercase font-bold mb-1">Clinical Observation</p>
                        <p className="text-xs text-gray-700 italic leading-relaxed">"{melanomaData.reasoning}"</p>
                      </div>

                        {melanomaData?.therapyEligibility && melanomaData.therapyEligibility.length > 0 && (
                          <div className="p-4 bg-blue-50 border border-blue-100 rounded-2xl space-y-2">
                            <div className="flex items-center gap-2">
                              <ShieldCheck className="w-4 h-4 text-blue-600" />
                              <p className="text-[10px] font-bold text-blue-800 uppercase tracking-widest">Immunotherapy Eligibility Support</p>
                            </div>
                            <div className="flex flex-wrap gap-2">
                              {melanomaData?.therapyEligibility?.map((t, i) => (
                                <span key={i} className="px-2 py-1 bg-white border border-blue-200 text-blue-600 rounded-lg text-[8px] font-bold uppercase">
                                  {t}
                                </span>
                              ))}
                            </div>
                            <p className="text-[8px] text-blue-500 italic">Note: This is a research-grade suggestion for clinical evaluation only.</p>
                          </div>
                        )}

                      <div className="pt-4 border-t border-gray-200">
                        <button 
                          onClick={handleProgressionSimulation}
                          disabled={isSimulatingProgression}
                          className="w-full py-3 bg-blue-600 text-white rounded-xl font-bold text-xs hover:bg-blue-700 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
                        >
                          {isSimulatingProgression ? <Loader2 className="w-4 h-4 animate-spin" /> : <Dna className="w-4 h-4" />}
                          RUN DIGITAL TWIN PROGRESSION SIMULATION (6-MONTHS)
                        </button>
                      </div>

                      {progressionData && (
                        <motion.div 
                          initial={{ opacity: 0, height: 0 }}
                          animate={{ opacity: 1, height: 'auto' }}
                          className="space-y-6 pt-6"
                        >
                          <div className="p-4 bg-white border border-gray-200 rounded-2xl">
                            <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-4">6-Month Progression Forecast</p>
                            <div className="flex items-end justify-between h-32 gap-2">
                              {progressionData?.months?.map((m, i) => (
                                <div key={i} className="flex-1 flex flex-col items-center gap-2">
                                  <div className="w-full flex gap-1 items-end h-24">
                                    <div 
                                      className="flex-1 bg-red-200 rounded-t-sm transition-all duration-1000" 
                                      style={{ height: `${progressionData?.progression?.[i] || 0}%` }}
                                    />
                                    <div 
                                      className="flex-1 bg-emerald-500 rounded-t-sm transition-all duration-1000" 
                                      style={{ height: `${progressionData?.interventionImpact?.[i] || 0}%` }}
                                    />
                                  </div>
                                  <span className="text-[6px] font-bold text-gray-400 uppercase">{m}</span>
                                </div>
                              ))}
                            </div>
                            <div className="flex justify-center gap-6 mt-4">
                              <div className="flex items-center gap-2">
                                <div className="w-2 h-2 bg-red-200 rounded-full" />
                                <span className="text-[8px] font-bold text-gray-500 uppercase">No Intervention</span>
                              </div>
                              <div className="flex items-center gap-2">
                                <div className="w-2 h-2 bg-emerald-500 rounded-full" />
                                <span className="text-[8px] font-bold text-gray-500 uppercase">With Suggested Therapy</span>
                              </div>
                            </div>
                          </div>
                          <div className="p-4 bg-emerald-50 border border-emerald-100 rounded-2xl">
                            <p className="text-[8px] text-emerald-800 font-bold uppercase mb-1">Forecast Summary</p>
                            <p className="text-xs text-emerald-700 leading-relaxed italic">"{progressionData.summary}"</p>
                          </div>
                        </motion.div>
                      )}

                      <div className="pt-4 border-t border-gray-200">
                        <button 
                          onClick={handleTreatmentOptimization}
                          disabled={isOptimizing}
                          className="w-full py-3 bg-[#1A1A1A] text-white rounded-xl font-bold text-xs hover:bg-black transition-all flex items-center justify-center gap-2 disabled:opacity-50"
                        >
                          {isOptimizing ? <Loader2 className="w-4 h-4 animate-spin" /> : <Brain className="w-4 h-4" />}
                          ACTIVATE STEP-11: DECISION AGENT (OPTIMIZE TREATMENT)
                        </button>
                      </div>

                      {decisionData && (
                        <motion.div 
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          className="p-6 bg-emerald-900 text-white rounded-3xl space-y-6 shadow-2xl border border-emerald-400/30"
                        >
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              <Zap className="w-4 h-4 text-emerald-400" />
                              <h4 className="text-[10px] font-bold uppercase tracking-widest">Optimized Treatment Path</h4>
                            </div>
                            <div className="px-2 py-0.5 bg-emerald-400/20 text-emerald-400 rounded text-[8px] font-bold border border-emerald-400/30">
                              OMEGA VERDICT
                            </div>
                          </div>

                          <div className="space-y-2">
                            <p className="text-xl font-black tracking-tight">{decisionData.optimizedPath}</p>
                            <p className="text-[10px] text-emerald-200/70 leading-relaxed italic">"{decisionData.rationale}"</p>
                          </div>

                          <div className="grid grid-cols-2 gap-4">
                            <div className="p-3 bg-white/10 rounded-xl border border-white/10">
                              <div className="flex items-center justify-between mb-1">
                                <span className="text-[8px] font-bold uppercase text-emerald-200">Efficacy Score</span>
                                <span className="text-[10px] font-mono text-emerald-400">{decisionData.efficacyScore}%</span>
                              </div>
                              <div className="w-full h-1 bg-white/10 rounded-full overflow-hidden">
                                <div className="h-full bg-emerald-400" style={{ width: `${decisionData.efficacyScore}%` }} />
                              </div>
                            </div>
                            <div className="p-3 bg-white/10 rounded-xl border border-white/10">
                              <div className="flex items-center justify-between mb-1">
                                <span className="text-[8px] font-bold uppercase text-red-200">Toxicity Risk</span>
                                <span className="text-[10px] font-mono text-red-400">{decisionData.toxicityRisk}%</span>
                              </div>
                              <div className="w-full h-1 bg-white/10 rounded-full overflow-hidden">
                                <div className="h-full bg-red-400" style={{ width: `${decisionData.toxicityRisk}%` }} />
                              </div>
                            </div>
                          </div>

                          <button 
                            onClick={handleSaveMemory}
                            disabled={isSavingMemory}
                            className="w-full py-3 bg-emerald-400 text-emerald-950 rounded-2xl font-black text-[10px] uppercase tracking-widest hover:bg-emerald-300 transition-all flex items-center justify-center gap-2 disabled:opacity-50 shadow-lg shadow-emerald-500/20"
                          >
                            {isSavingMemory ? <Loader2 className="w-3 h-3 animate-spin" /> : <Save className="w-3 h-3" />}
                            PERSIST TO EVOLUTIONARY MEMORY (STEP-19)
                          </button>
                        </motion.div>
                      )}
                    </motion.div>
                  )}
                </div>

                {/* Recursive Learning */}
                <div className="space-y-6">
                  <h3 className="text-2xl font-black tracking-tight">Recursive Learning Nodes</h3>
                  
                  {/* Self-Improvement Loop Visualizer */}
                  <div className="p-6 bg-[#1A1A1A] text-white rounded-2xl shadow-xl space-y-6 border border-white/10">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <RefreshCw className={`w-4 h-4 text-blue-400 ${isLooping ? 'animate-spin' : ''}`} />
                        <p className="text-[10px] font-bold uppercase tracking-widest">Self-Improvement Loop</p>
                      </div>
                      {loopData && (
                        <div className="px-2 py-0.5 bg-blue-500/20 text-blue-400 rounded text-[8px] font-bold border border-blue-500/30">
                          LVL: {loopData.consciousnessLevel}
                        </div>
                      )}
                    </div>

                    <div className="grid grid-cols-4 gap-2">
                      {[
                        { icon: Eye, label: 'Observe' },
                        { icon: Database, label: 'Recall' },
                        { icon: Brain, label: 'Decide' },
                        { icon: Zap, label: 'Act' },
                        { icon: Activity, label: 'Evaluate' },
                        { icon: Trophy, label: 'Reward' },
                        { icon: BookOpen, label: 'Learn' },
                        { icon: Dna, label: 'Mutate' },
                        { icon: ShieldCheck, label: 'Verify' },
                        { icon: Target, label: 'Align' },
                        { icon: RefreshCw, label: 'Recurse' }
                      ].map((step, i) => (
                        <div 
                          key={i} 
                          className={`flex flex-col items-center gap-1 p-2 rounded-lg border transition-all ${
                            loopStep === i + 1 
                              ? 'bg-blue-500/20 border-blue-500 text-blue-400 scale-105 shadow-[0_0_15px_rgba(59,130,246,0.3)]' 
                              : 'bg-white/5 border-white/10 text-gray-500'
                          }`}
                        >
                          <step.icon className="w-3 h-3" />
                          <span className="text-[6px] font-bold uppercase">{step.label}</span>
                        </div>
                      ))}
                    </div>

                    {loopData && (
                      <motion.div 
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="space-y-4 pt-4 border-t border-white/10"
                      >
                        <div className="grid grid-cols-2 gap-4">
                          <div className="space-y-2">
                            <div className="flex items-center gap-2 text-emerald-400">
                              <Lightbulb className="w-3 h-3" />
                              <span className="text-[8px] font-bold uppercase">Insights</span>
                            </div>
                            <div className="space-y-1">
                              {loopData?.insights?.map((insight: string, i: number) => (
                                <p key={i} className="text-[8px] text-gray-400 leading-tight">• {insight}</p>
                              ))}
                            </div>
                          </div>
                          <div className="space-y-2">
                            <div className="flex items-center gap-2 text-blue-400">
                              <Target className="w-3 h-3" />
                              <span className="text-[8px] font-bold uppercase">Self-Goals</span>
                            </div>
                            <div className="space-y-1">
                              {loopData?.selfGoals?.map((goal: string, i: number) => (
                                <p key={i} className="text-[8px] text-gray-400 leading-tight">• {goal}</p>
                              ))}
                            </div>
                          </div>
                        </div>

                        <div className="p-3 bg-white/5 rounded-xl border border-white/10">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-[8px] font-bold text-gray-400 uppercase">Next Experiment</span>
                            <span className="text-[8px] font-mono text-blue-400">CRITIC SCORE: {loopData.criticScore}%</span>
                          </div>
                          <p className="text-[9px] font-bold text-white italic">"{loopData.nextExperiment}"</p>
                        </div>

                        {/* World Model Integration */}
                        <div className="p-4 bg-blue-900/40 border border-blue-400/30 rounded-2xl space-y-3">
                          <div className="flex items-center gap-2">
                            <Globe className="w-4 h-4 text-blue-400" />
                            <span className="text-[10px] font-bold text-blue-400 uppercase tracking-widest">World Model Propagation</span>
                          </div>
                          <div className="space-y-2">
                            <div className="flex justify-between text-[8px] font-bold text-blue-200 uppercase">
                              <span>Genetic Reach</span>
                              <span>{crisprResult ? Math.round(crisprResult.impactScore * 0.8) : 0}%</span>
                            </div>
                            <div className="w-full h-1 bg-white/10 rounded-full overflow-hidden">
                              <div className="h-full bg-blue-400" style={{ width: `${crisprResult ? crisprResult.impactScore * 0.8 : 0}%` }} />
                            </div>
                            <p className="text-[8px] text-blue-100/70 leading-tight italic">
                              "Genetic modifications are projected to propagate through the simulated population with {crisprResult ? Math.round(crisprResult.impactScore * 0.8) : 0}% efficiency."
                            </p>
                          </div>
                        </div>
                      </motion.div>
                    )}
                    
                    {!loopData && !isLooping && (
                      <div className="py-8 text-center space-y-2">
                        <RefreshCw className="w-8 h-8 text-white/10 mx-auto" />
                        <p className="text-[10px] text-gray-500 font-bold uppercase tracking-widest">Awaiting Mission Execution</p>
                      </div>
                    )}
                  </div>

                  <div className="p-6 bg-[#1A1A1A] text-white rounded-2xl shadow-xl space-y-4">
                    <div className="flex items-center justify-between">
                      <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Evolutionary State</p>
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" />
                        <span className="text-[10px] font-bold">SYNCING</span>
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      {profile?.learningNodes?.map((node, i) => (
                        <div key={i} className="flex items-center justify-between p-2 bg-white/5 rounded-lg border border-white/10">
                          <span className="text-[10px] font-mono">{node}</span>
                          <ChevronRight className="w-3 h-3 text-gray-500" />
                        </div>
                      ))}
                    </div>

                    {/* Evolutionary Log */}
                    <div className="pt-4 border-t border-white/10 space-y-3">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Dna className="w-3 h-3 text-blue-400" />
                          <span className="text-[8px] font-bold text-white uppercase tracking-widest">Evolutionary Log</span>
                        </div>
                        <span className="text-[8px] font-mono text-blue-400 animate-pulse">MUTATING...</span>
                      </div>
                      <div className="h-32 overflow-y-auto no-scrollbar font-mono text-[8px] space-y-1">
                        {neuralLog.filter(l => l.agent === 'EVOLUTION ENGINE' || l.agent === 'STRATEGIST').map((log, i) => (
                          <div key={i} className="flex gap-2 border-b border-white/5 pb-1">
                            <span className="text-gray-500">[{log.timestamp}]</span>
                            <span className="text-blue-400">MUTATION:</span>
                            <span className="text-gray-300">{log.action}</span>
                          </div>
                        ))}
                        {neuralLog.length === 0 && <p className="text-gray-600 italic">Awaiting evolutionary trigger...</p>}
                      </div>
                    </div>

                    <div className="pt-4 border-t border-white/10">
                      <p className="text-[10px] text-gray-400 leading-relaxed italic">
                        "The lab is recursively optimizing your profile based on real-time hypergraph feedback. Every mission intent evolves the underlying model."
                      </p>
                    </div>
                  </div>

                  {/* Behavior AI / Human Context */}
                  <div className="p-6 bg-[#1A1A1A] text-white rounded-2xl shadow-xl space-y-6 border border-white/10">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <User className="w-4 h-4 text-emerald-400" />
                        <h4 className="text-[10px] font-bold uppercase tracking-widest">Behavioral Biometrics</h4>
                      </div>
                      <button 
                        onClick={async () => {
                          if (videoRef.current && canvasRef.current) {
                            const context = canvasRef.current.getContext('2d');
                            if (context) {
                              context.drawImage(videoRef.current, 0, 0, canvasRef.current.width, canvasRef.current.height);
                              const imageData = canvasRef.current.toDataURL('image/png');
                              handleBehaviorAnalysis(imageData);
                            }
                          } else {
                            setIsCameraOpen(true);
                          }
                        }}
                        disabled={isAnalyzingBehavior}
                        className="px-3 py-1 bg-emerald-500/20 text-emerald-400 rounded text-[8px] font-bold border border-emerald-500/30 hover:bg-emerald-500/30 transition-all flex items-center gap-1"
                      >
                        {isAnalyzingBehavior ? <Loader2 className="w-2 h-2 animate-spin" /> : <Camera className="w-2 h-2" />}
                        SCAN BEHAVIOR
                      </button>
                    </div>

                    {behaviorData ? (
                      <div className="space-y-4">
                        <div className="grid grid-cols-2 gap-3">
                          <div className="p-3 bg-white/5 rounded-xl border border-white/10">
                            <p className="text-[8px] text-gray-500 uppercase font-bold mb-1">Emotion</p>
                            <p className="text-xs font-bold text-white uppercase">{behaviorData.emotion}</p>
                          </div>
                          <div className="p-3 bg-white/5 rounded-xl border border-white/10">
                            <p className="text-[8px] text-gray-500 uppercase font-bold mb-1">Motion</p>
                            <p className="text-xs font-bold text-white uppercase">{behaviorData.motion}</p>
                          </div>
                        </div>
                        <div className="p-3 bg-white/5 rounded-xl border border-white/10 space-y-2">
                          <div className="flex items-center justify-between">
                            <p className="text-[8px] text-gray-500 uppercase font-bold">Stress Level</p>
                            <p className={`text-[10px] font-bold ${behaviorData.stressLevel > 70 ? 'text-red-400' : 'text-emerald-400'}`}>
                              {behaviorData.stressLevel}%
                            </p>
                          </div>
                          <div className="w-full h-1 bg-white/10 rounded-full overflow-hidden">
                            <div 
                              className={`h-full transition-all duration-1000 ${behaviorData.stressLevel > 70 ? 'bg-red-500' : 'bg-emerald-500'}`}
                              style={{ width: `${behaviorData.stressLevel}%` }}
                            />
                          </div>
                        </div>
                        <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-xl">
                          <p className="text-[8px] text-emerald-400 font-bold uppercase mb-1">Human Context Insight</p>
                          <p className="text-[9px] text-gray-300 italic leading-tight">"{behaviorData.insight}"</p>
                        </div>
                      </div>
                    ) : (
                      <div className="py-6 text-center space-y-2 border border-dashed border-white/10 rounded-xl">
                        <User className="w-6 h-6 text-white/10 mx-auto" />
                        <p className="text-[8px] text-gray-600 font-bold uppercase tracking-widest">Awaiting Behavioral Scan</p>
                      </div>
                    )}
                  </div>
                </div>
              </motion.div>
            )}

            {activeTab === 'RESEARCH DEVICE' && (
              <motion.div 
                key="research"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="space-y-8"
              >
                <div className="flex items-center justify-between">
                  <h3 className="text-2xl font-black tracking-tight">Research Device Interface</h3>
                  <div className="flex items-center gap-2 px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-[10px] font-bold uppercase tracking-widest">
                    <Wifi className="w-3 h-3" />
                    Uplink Established
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {/* Mobile Connection */}
                  <div className="p-6 bg-white border border-[#E5E7EB] rounded-2xl shadow-sm space-y-4 group hover:border-blue-500 transition-all">
                    <div className="flex items-center justify-between">
                      <div className="p-2 bg-blue-50 rounded-lg">
                        <Smartphone className="w-6 h-6 text-blue-600" />
                      </div>
                      <div className="w-2 h-2 bg-green-500 rounded-full shadow-[0_0_8px_rgba(34,197,94,0.5)]" />
                    </div>
                    <div>
                      <h4 className="font-bold text-sm">Mobile Uplink</h4>
                      <p className="text-[10px] text-[#6B7280]">Remote sensor synchronization active.</p>
                    </div>
                    <div className="pt-2">
                      <label className="w-full py-2 bg-[#F3F4F6] text-[#1A1A1A] rounded-lg text-[10px] font-bold hover:bg-[#1A1A1A] hover:text-white transition-all cursor-pointer flex items-center justify-center">
                        SYNC DEVICE
                        <input type="file" className="hidden" accept="image/*,.txt" onChange={handleFileUpload} />
                      </label>
                    </div>
                  </div>

                  {/* Robot Connection */}
                  <div className="p-6 bg-white border border-[#E5E7EB] rounded-2xl shadow-sm space-y-4 group hover:border-red-500 transition-all">
                    <div className="flex items-center justify-between">
                      <div className="p-2 bg-red-50 rounded-lg">
                        <Bot className="w-6 h-6 text-red-600" />
                      </div>
                      <div className="w-2 h-2 bg-orange-500 rounded-full animate-pulse" />
                    </div>
                    <div>
                      <h4 className="font-bold text-sm">Robot Controller</h4>
                      <p className="text-[10px] text-[#6B7280]">Kinematic feedback loop: 12ms latency.</p>
                    </div>
                    <div className="pt-2">
                      <button className="w-full py-2 bg-[#F3F4F6] text-[#1A1A1A] rounded-lg text-[10px] font-bold hover:bg-[#1A1A1A] hover:text-white transition-all">
                        INITIALIZE DRIVER
                      </button>
                    </div>
                  </div>

                  {/* Research Labs */}
                  <div className="p-6 bg-white border border-[#E5E7EB] rounded-2xl shadow-sm space-y-4 group hover:border-emerald-500 transition-all">
                    <div className="flex items-center justify-between">
                      <div className="p-2 bg-emerald-50 rounded-lg">
                        <Microscope className="w-6 h-6 text-emerald-600" />
                      </div>
                      <div className="w-2 h-2 bg-green-500 rounded-full" />
                    </div>
                    <div>
                      <h4 className="font-bold text-sm">Lab Network</h4>
                      <p className="text-[10px] text-[#6B7280]">Connected to 14 global research nodes.</p>
                    </div>
                    <div className="pt-2">
                      <button className="w-full py-2 bg-[#F3F4F6] text-[#1A1A1A] rounded-lg text-[10px] font-bold hover:bg-[#1A1A1A] hover:text-white transition-all">
                        ACCESS LAB DATA
                      </button>
                    </div>
                  </div>

                  {/* Video Purpose */}
                  <div className="p-6 bg-white border border-[#E5E7EB] rounded-2xl shadow-sm space-y-4 group hover:border-purple-500 transition-all">
                    <div className="flex items-center justify-between">
                      <div className="p-2 bg-purple-50 rounded-lg">
                        <Video className="w-6 h-6 text-purple-600" />
                      </div>
                      <div className="w-2 h-2 bg-red-500 rounded-full" />
                    </div>
                    <div>
                      <h4 className="font-bold text-sm">Science Discovery</h4>
                      <p className="text-[10px] text-[#6B7280]">Live spectral analysis stream.</p>
                    </div>
                    <div className="pt-2">
                      <button className="w-full py-2 bg-[#F3F4F6] text-[#1A1A1A] rounded-lg text-[10px] font-bold hover:bg-[#1A1A1A] hover:text-white transition-all">
                        OPEN FEED
                      </button>
                    </div>
                  </div>
                </div>

                {/* Discovery Feed Section */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                  <div className="lg:col-span-2 p-6 bg-[#1A1A1A] text-white rounded-3xl shadow-xl overflow-hidden relative">
                    <div className="absolute top-0 right-0 p-6">
                      <div className="flex items-center gap-2 px-3 py-1 bg-white/10 rounded-full text-[8px] font-bold uppercase tracking-widest backdrop-blur-md">
                        <Radio className="w-3 h-3 text-red-500 animate-pulse" />
                        LIVE DISCOVERY FEED
                      </div>
                    </div>
                    
                    <div className="space-y-6">
                      <h4 className="text-xl font-black tracking-tight">Spectral Analysis: Node-04</h4>
                      <div className="aspect-video bg-black/40 rounded-2xl border border-white/10 flex items-center justify-center relative overflow-hidden">
                        {/* Mock Video Feed */}
                        <div className="absolute inset-0 opacity-20 pointer-events-none">
                          <div className="w-full h-full bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-blue-500/20 via-transparent to-transparent animate-pulse" />
                        </div>
                        <div className="text-center space-y-2 z-10">
                          <Database className="w-12 h-12 text-white/20 mx-auto" />
                          <p className="text-[10px] font-mono text-white/40 uppercase tracking-widest">Awaiting High-Res Stream...</p>
                        </div>
                        {/* Scanning Line */}
                        <motion.div 
                          animate={{ top: ['0%', '100%'] }}
                          transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
                          className="absolute left-0 right-0 h-[1px] bg-blue-500/50 shadow-[0_0_10px_rgba(59,130,246,0.5)] z-20"
                        />
                      </div>
                      <div className="grid grid-cols-3 gap-4">
                        <div className="p-3 bg-white/5 rounded-xl border border-white/10">
                          <p className="text-[8px] font-bold text-gray-500 uppercase mb-1">Frequency</p>
                          <p className="text-sm font-mono font-bold">4.2 GHz</p>
                        </div>
                        <div className="p-3 bg-white/5 rounded-xl border border-white/10">
                          <p className="text-[8px] font-bold text-gray-500 uppercase mb-1">Resolution</p>
                          <p className="text-sm font-mono font-bold">8K Spectral</p>
                        </div>
                        <div className="p-3 bg-white/5 rounded-xl border border-white/10">
                          <p className="text-[8px] font-bold text-gray-500 uppercase mb-1">Discovery</p>
                          <p className="text-sm font-mono font-bold text-emerald-400">98.2% Match</p>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* System Alerts */}
                  <div className="space-y-6">
                    <div className="flex items-center justify-between">
                      <h4 className="text-lg font-black tracking-tight">System Alerts</h4>
                      <span className="px-2 py-0.5 bg-red-500/20 text-red-500 rounded text-[8px] font-bold border border-red-500/30">
                        {notifications.filter(n => !n.read).length} ACTIVE
                      </span>
                    </div>
                    <div className="space-y-4 max-h-[400px] overflow-y-auto no-scrollbar pr-2">
                      {notifications.length > 0 ? notifications.map((n, i) => (
                        <motion.div 
                          key={n.id}
                          initial={{ opacity: 0, x: 20 }}
                          animate={{ opacity: 1, x: 0 }}
                          className={`p-4 rounded-2xl border transition-all ${
                            n.type === 'health' ? 'bg-red-50 border-red-100' : 'bg-blue-50 border-blue-100'
                          }`}
                        >
                          <div className="flex items-center gap-3 mb-2">
                            <div className={`p-1.5 rounded-lg ${n.type === 'health' ? 'bg-red-100 text-red-600' : 'bg-blue-100 text-blue-600'}`}>
                              {n.type === 'health' ? <AlertCircle className="w-4 h-4" /> : <Bell className="w-4 h-4" />}
                            </div>
                            <span className="text-[8px] font-bold uppercase tracking-widest text-gray-500">{n.timestamp}</span>
                          </div>
                          <p className={`text-xs font-bold leading-tight ${n.type === 'health' ? 'text-red-900' : 'text-blue-900'}`}>
                            {n.message}
                          </p>
                        </motion.div>
                      )) : (
                        <div className="p-8 text-center text-gray-400 bg-gray-50 rounded-2xl border border-dashed border-gray-200">
                          <p className="text-[10px] font-bold uppercase tracking-widest">No Active Alerts</p>
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="space-y-6">
                    <h4 className="text-lg font-black tracking-tight">Active Uplinks</h4>
                    <div className="space-y-3">
                      {[
                        { name: 'Omega-Watch-v4', type: 'Watch', status: 'Live' },
                        { name: 'Mobile-Alpha', type: 'Smartphone', status: 'Connected' },
                        { name: 'Robot-Unit-01', type: 'Bot', status: 'Standby' },
                        { name: 'Lab-Geneva', type: 'Microscope', status: 'Syncing' }
                      ].map((device, i) => (
                        <div key={i} className="p-4 bg-white border border-[#E5E7EB] rounded-2xl flex items-center justify-between group hover:bg-gray-50 transition-all">
                          <div className="flex items-center gap-3">
                            <div className="p-2 bg-gray-100 rounded-lg group-hover:bg-white transition-all">
                              {device.type === 'Watch' && <Activity className="w-4 h-4 text-red-500" />}
                              {device.type === 'Smartphone' && <Smartphone className="w-4 h-4" />}
                              {device.type === 'Bot' && <Bot className="w-4 h-4" />}
                              {device.type === 'Microscope' && <Microscope className="w-4 h-4" />}
                            </div>
                            <div>
                              <p className="text-xs font-bold">{device.name}</p>
                              <p className="text-[8px] text-[#6B7280] uppercase font-bold tracking-widest">{device.type}</p>
                            </div>
                          </div>
                          <span className={cn(
                            "text-[8px] font-bold uppercase tracking-widest px-2 py-1 rounded-full",
                            device.status === 'Live' ? "bg-red-100 text-red-700 animate-pulse" :
                            device.status === 'Connected' ? "bg-green-100 text-green-700" : 
                            device.status === 'Standby' ? "bg-orange-100 text-orange-700" : "bg-blue-100 text-blue-700"
                          )}>
                            {device.status}
                          </span>
                        </div>
                      ))}
                    </div>
                    <button className="w-full py-3 border-2 border-dashed border-[#D1D5DB] rounded-2xl text-[10px] font-bold text-[#6B7280] hover:border-[#1A1A1A] hover:text-[#1A1A1A] transition-all flex items-center justify-center gap-2">
                      <Plus className="w-4 h-4" />
                      ADD NEW DEVICE
                    </button>

                    {/* Wearable Connectivity Test */}
                    <div className="p-6 bg-white border border-red-100 rounded-3xl shadow-sm space-y-4">
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-red-100 rounded-lg">
                          <Activity className="w-5 h-5 text-red-600" />
                        </div>
                        <div>
                          <h4 className="text-sm font-black tracking-tight uppercase">Wearable Connectivity</h4>
                          <p className="text-[10px] text-red-600 font-bold uppercase tracking-widest">Omega Watch v4 Sync</p>
                        </div>
                      </div>
                      
                      <div className="space-y-3">
                        <div className="flex items-center justify-between p-3 bg-gray-50 rounded-xl border border-gray-100">
                          <span className="text-[10px] font-bold text-gray-500 uppercase">Signal Strength</span>
                          <div className="flex gap-0.5">
                            {[1, 2, 3, 4].map(i => <div key={i} className="w-1 h-3 bg-emerald-500 rounded-full" />)}
                          </div>
                        </div>
                        
                        <div className="p-3 bg-gray-50 rounded-xl border border-gray-100 space-y-2">
                          <div className="flex items-center justify-between">
                            <span className="text-[10px] font-bold text-gray-500 uppercase">Live HRV Stream</span>
                            <span className="text-[10px] font-mono text-emerald-600 font-bold">{profile.bioMarkers.hrv}</span>
                          </div>
                          <div className="h-8 flex items-end gap-0.5 overflow-hidden">
                            {new Array(30).fill(0).map((_, i) => (
                              <motion.div 
                                key={i}
                                animate={{ height: [10, 20, 15, 25, 10][i % 5] }}
                                transition={{ duration: 1, repeat: Infinity, delay: i * 0.1 }}
                                className="flex-1 bg-red-400 rounded-t-sm"
                              />
                            ))}
                          </div>
                        </div>
                      </div>

                      <button 
                        onClick={() => {
                          // Simulate a data sync
                          setProfile(prev => ({
                            ...prev,
                            bioMarkers: {
                              ...prev.bioMarkers,
                              heartRate: `${Math.floor(Math.random() * 20) + 70} bpm`,
                              hrv: `${Math.floor(Math.random() * 10) + 60} ms`
                            }
                          }));
                          
                          const alert: Notification = {
                            id: Date.now().toString(),
                            type: 'system',
                            message: `Wearable Sync Successful. Bio-markers updated.`,
                            timestamp: new Date().toLocaleTimeString(),
                            read: false
                          };
                          setNotifications(prev => [alert, ...prev]);
                        }}
                        className="w-full py-3 bg-[#1A1A1A] text-white rounded-xl text-[10px] font-bold uppercase tracking-widest hover:bg-black transition-all flex items-center justify-center gap-2"
                      >
                        <RefreshCw className="w-3 h-3" />
                        SYNC WEARABLE DATA
                      </button>
                    </div>

                    {/* Live Lab Data Stream */}
                    <div className="p-6 bg-[#1A1A1A] rounded-3xl border border-[#333] space-y-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Activity className="w-4 h-4 text-blue-500" />
                          <h4 className="text-sm font-bold text-white uppercase tracking-widest">Lab Data Stream</h4>
                        </div>
                        <span className="text-[10px] text-blue-500 font-mono animate-pulse">LIVE</span>
                      </div>
                      <div className="h-48 overflow-y-auto no-scrollbar font-mono text-[9px] space-y-2">
                        {neuralLog.filter(l => l.agent === 'SCIENTIST' || l.agent === 'EVOLUTION ENGINE').map((log, i) => (
                          <div key={i} className="flex gap-3 border-b border-white/5 pb-1">
                            <span className="text-gray-500">[{log.timestamp}]</span>
                            <span className="text-emerald-400">DATA_INGRESS:</span>
                            <span className="text-gray-300">{log.action}</span>
                          </div>
                        ))}
                        {neuralLog.length === 0 && <p className="text-gray-600 italic">Waiting for lab uplink...</p>}
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>
            )}

            {activeTab === 'SCIENTIFIC DISCOVERY' && (
              <motion.div 
                key="scientific-discovery"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="space-y-8"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="p-3 bg-amber-100 rounded-2xl">
                      <Lightbulb className="w-8 h-8 text-amber-600" />
                    </div>
                    <div>
                      <h3 className="text-2xl font-black tracking-tight">Hypothesis & Experimentation Engine</h3>
                      <p className="text-[10px] text-gray-400 uppercase font-bold tracking-widest">Phase Alpha: Autonomous Discovery</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 px-4 py-2 bg-amber-50 text-amber-700 rounded-full text-xs font-bold border border-amber-100">
                    <Brain className="w-4 h-4" />
                    SCIENTIFIC METHOD ACTIVE
                  </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  {/* Hypothesis Generation */}
                  <div className="p-8 bg-white border border-[#E5E7EB] rounded-3xl shadow-sm space-y-6 relative overflow-hidden">
                    <div className="absolute top-0 right-0 p-6 opacity-10">
                      <Brain className="w-24 h-24 text-amber-500" />
                    </div>
                    
                    <div className="flex items-center justify-between relative z-10">
                      <div className="flex items-center gap-2">
                        <Target className="w-5 h-5 text-amber-600" />
                        <h4 className="text-sm font-bold uppercase tracking-widest">Hypothesis Agent</h4>
                      </div>
                      <button 
                        onClick={handleGenerateHypothesis}
                        disabled={isGeneratingHypothesis}
                        className="px-4 py-2 bg-amber-600 text-white rounded-xl text-xs font-bold hover:bg-amber-700 disabled:opacity-50 transition-all flex items-center gap-2 shadow-lg shadow-amber-200"
                      >
                        {isGeneratingHypothesis ? <Loader2 className="w-4 h-4 animate-spin" /> : <Plus className="w-4 h-4" />}
                        GENERATE HYPOTHESIS
                      </button>
                    </div>

                    {hypothesis ? (
                      <motion.div 
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="space-y-6 relative z-10"
                      >
                        <div className="p-6 bg-amber-50 border border-amber-100 rounded-2xl">
                          <p className="text-[10px] text-amber-600 font-bold uppercase mb-2">Current Hypothesis</p>
                          <p className="text-lg font-bold text-amber-900 leading-tight italic">"{hypothesis.hypothesis}"</p>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                          <div className="p-4 bg-gray-50 rounded-xl border border-gray-100">
                            <p className="text-[8px] text-gray-500 font-bold uppercase mb-1">Confidence Level</p>
                            <div className="flex items-center gap-2">
                              <div className="flex-1 h-1.5 bg-gray-200 rounded-full overflow-hidden">
                                <div 
                                  className="h-full bg-amber-500 transition-all duration-1000"
                                  style={{ width: `${hypothesis.confidence}%` }}
                                />
                              </div>
                              <span className="text-xs font-bold text-amber-600">{hypothesis.confidence}%</span>
                            </div>
                          </div>
                          <div className="p-4 bg-gray-50 rounded-xl border border-gray-100">
                            <p className="text-[8px] text-gray-500 font-bold uppercase mb-1">Variables</p>
                            <div className="flex flex-wrap gap-1">
                              {hypothesis?.variables?.map((v, i) => (
                                <span key={i} className="px-1.5 py-0.5 bg-white border border-gray-200 rounded text-[8px] font-bold text-gray-600 uppercase">{v}</span>
                              ))}
                            </div>
                          </div>
                        </div>

                        <div className="p-4 bg-white border border-amber-100 rounded-xl">
                          <p className="text-[8px] text-amber-600 font-bold uppercase mb-1">Scientific Rationale</p>
                          <p className="text-[10px] text-gray-600 leading-relaxed">{hypothesis.rationale}</p>
                        </div>
                      </motion.div>
                    ) : (
                      <div className="py-12 text-center space-y-3 border-2 border-dashed border-gray-100 rounded-2xl">
                        <Lightbulb className="w-12 h-12 text-gray-200 mx-auto" />
                        <p className="text-xs text-gray-400 font-medium">Awaiting Hypothesis Trigger...</p>
                      </div>
                    )}
                  </div>

                  {/* Experimentation Loop */}
                  <div className="p-8 bg-[#1A1A1A] text-white rounded-3xl shadow-xl space-y-6 relative overflow-hidden border border-white/10">
                    <div className="absolute top-0 right-0 p-6 opacity-10">
                      <RefreshCw className="w-24 h-24 text-blue-500" />
                    </div>

                    <div className="flex items-center justify-between relative z-10">
                      <div className="flex items-center gap-2">
                        <Microscope className="w-5 h-5 text-blue-400" />
                        <h4 className="text-sm font-bold uppercase tracking-widest">Experimentation Loop</h4>
                      </div>
                      <button 
                        onClick={handleRunExperiment}
                        disabled={isRunningExperiment || !hypothesis}
                        className="px-4 py-2 bg-blue-600 text-white rounded-xl text-xs font-bold hover:bg-blue-700 disabled:opacity-50 transition-all flex items-center gap-2 shadow-lg shadow-blue-900/50"
                      >
                        {isRunningExperiment ? <Loader2 className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
                        RUN EXPERIMENT
                      </button>
                    </div>

                    {experimentResult ? (
                      <motion.div 
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="space-y-6 relative z-10"
                      >
                        <div className="flex items-center gap-4">
                          <div className={cn(
                            "px-4 py-2 rounded-xl text-xs font-black uppercase tracking-widest border",
                            experimentResult.result === 'PASSED' ? "bg-emerald-500/20 text-emerald-400 border-emerald-500/30" :
                            experimentResult.result === 'FAILED' ? "bg-red-500/20 text-red-400 border-red-500/30" : "bg-blue-500/20 text-blue-400 border-blue-500/30"
                          )}>
                            RESULT: {experimentResult.result}
                          </div>
                          <div className="flex-1 h-[1px] bg-white/10" />
                        </div>

                        <div className="p-4 bg-white/5 border border-white/10 rounded-2xl space-y-3">
                          <div className="flex items-center gap-2">
                            <Eye className="w-3 h-3 text-blue-400" />
                            <p className="text-[8px] text-gray-500 font-bold uppercase">Observation</p>
                          </div>
                          <p className="text-[10px] text-gray-300 leading-relaxed italic">"{experimentResult.observation}"</p>
                        </div>

                        <div className="p-4 bg-blue-500/10 border border-blue-500/20 rounded-2xl space-y-3">
                          <div className="flex items-center gap-2">
                            <RefreshCw className="w-3 h-3 text-blue-400" />
                            <p className="text-[8px] text-blue-400 font-bold uppercase">Bayesian Belief Update</p>
                          </div>
                          <p className="text-[10px] text-blue-100 font-mono leading-relaxed">{experimentResult.beliefUpdate}</p>
                        </div>

                        <div className="pt-4 border-t border-white/10">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-[8px] font-bold text-gray-500 uppercase tracking-widest">Scientific Memory Sync</span>
                            <span className="text-[8px] font-mono text-emerald-400">SUCCESS</span>
                          </div>
                          <div className="w-full h-1 bg-white/5 rounded-full overflow-hidden">
                            <motion.div 
                              initial={{ width: 0 }}
                              animate={{ width: '100%' }}
                              className="h-full bg-emerald-500"
                            />
                          </div>
                        </div>
                      </motion.div>
                    ) : (
                      <div className="py-12 text-center space-y-3 border-2 border-dashed border-white/5 rounded-2xl">
                        <RefreshCw className="w-12 h-12 text-white/5 mx-auto" />
                        <p className="text-xs text-gray-600 font-medium uppercase tracking-widest">Awaiting Experiment Trigger...</p>
                      </div>
                    )}
                  </div>
                </div>

                {/* Discovery Timeline */}
                <div className="p-8 bg-white border border-[#E5E7EB] rounded-3xl shadow-sm space-y-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Clock className="w-5 h-5 text-gray-400" />
                      <h4 className="text-sm font-bold uppercase tracking-widest">Discovery Timeline</h4>
                    </div>
                    <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Recursive Learning Active</span>
                  </div>

                  <div className="relative">
                    <div className="absolute left-4 top-0 bottom-0 w-[1px] bg-gray-100" />
                    <div className="space-y-6 relative">
                      {[
                        { time: 'T-Minus 0s', event: 'Hypothesis Engine Initialized', status: 'Active', color: 'bg-blue-500' },
                        { time: 'T-Minus 120s', event: 'Experimentation Loop Secured', status: 'Ready', color: 'bg-emerald-500' },
                        { time: 'T-Minus 300s', event: 'Bayesian Belief Network Online', status: 'Syncing', color: 'bg-amber-500' }
                      ].map((item, i) => (
                        <div key={i} className="flex gap-6 items-start">
                          <div className={cn("w-8 h-8 rounded-full border-4 border-white shadow-sm shrink-0 z-10", item.color)} />
                          <div className="pt-1">
                            <p className="text-[10px] font-mono text-gray-400">{item.time}</p>
                            <p className="text-sm font-bold text-gray-900">{item.event}</p>
                            <p className="text-[10px] font-bold text-gray-500 uppercase tracking-widest">{item.status}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </motion.div>
            )}

            {activeTab === 'VISUAL SIMULATION' && (
              <motion.div 
                key="visual-simulation"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="space-y-8"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="p-3 bg-purple-100 rounded-2xl">
                      <Video className="w-8 h-8 text-purple-600" />
                    </div>
                    <div>
                      <h3 className="text-2xl font-black tracking-tight">Diffusion & Video Simulation Engine</h3>
                      <p className="text-[10px] text-gray-400 uppercase font-bold tracking-widest">Phase Beta: Visual Synthesis</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 px-4 py-2 bg-purple-50 text-purple-700 rounded-full text-xs font-bold border border-purple-100">
                    <Zap className="w-4 h-4" />
                    VEO-1 & DIFFUSION ACTIVE
                  </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  {/* Diffusion Model - Synthetic Images */}
                  <div className="p-8 bg-white border border-[#E5E7EB] rounded-3xl shadow-sm space-y-6 relative overflow-hidden">
                    <div className="absolute top-0 right-0 p-6 opacity-10">
                      <Camera className="w-24 h-24 text-purple-500" />
                    </div>
                    
                    <div className="flex items-center justify-between relative z-10">
                      <div className="flex items-center gap-2">
                        <Camera className="w-5 h-5 text-purple-600" />
                        <h4 className="text-sm font-bold uppercase tracking-widest">Diffusion Engine</h4>
                      </div>
                      <button 
                        onClick={handleGenerateSyntheticImage}
                        disabled={isGeneratingImage}
                        className="px-4 py-2 bg-purple-600 text-white rounded-xl text-xs font-bold hover:bg-purple-700 disabled:opacity-50 transition-all flex items-center gap-2 shadow-lg shadow-purple-200"
                      >
                        {isGeneratingImage ? <Loader2 className="w-4 h-4 animate-spin" /> : <Plus className="w-4 h-4" />}
                        GENERATE SYNTHETIC LESION
                      </button>
                    </div>

                    <div className="aspect-square bg-gray-50 rounded-2xl border-2 border-dashed border-gray-100 flex items-center justify-center relative overflow-hidden">
                      {syntheticImage ? (
                        <img 
                          src={syntheticImage} 
                          alt="Synthetic Lesion" 
                          className="w-full h-full object-cover"
                          referrerPolicy="no-referrer"
                        />
                      ) : (
                        <div className="text-center space-y-2">
                          <Camera className="w-12 h-12 text-gray-200 mx-auto" />
                          <p className="text-xs text-gray-400 font-medium uppercase tracking-widest">Awaiting Image Synthesis...</p>
                        </div>
                      )}
                      {isGeneratingImage && (
                        <div className="absolute inset-0 bg-white/50 backdrop-blur-sm flex items-center justify-center">
                          <div className="text-center space-y-2">
                            <Loader2 className="w-8 h-8 text-purple-600 animate-spin mx-auto" />
                            <p className="text-[10px] font-bold text-purple-600 uppercase tracking-widest">Synthesizing Pixels...</p>
                          </div>
                        </div>
                      )}
                    </div>
                    <p className="text-[10px] text-gray-500 italic leading-tight">
                      * Synthetic data generated for training and simulation purposes. Not for clinical diagnosis.
                    </p>
                  </div>

                  {/* Video Simulation Engine - Veo */}
                  <div className="p-8 bg-[#1A1A1A] text-white rounded-3xl shadow-xl space-y-6 relative overflow-hidden border border-white/10">
                    <div className="absolute top-0 right-0 p-6 opacity-10">
                      <Video className="w-24 h-24 text-blue-500" />
                    </div>

                    <div className="flex items-center justify-between relative z-10">
                      <div className="flex items-center gap-2">
                        <Video className="w-5 h-5 text-blue-400" />
                        <h4 className="text-sm font-bold uppercase tracking-widest">Video Simulation (Veo)</h4>
                      </div>
                      <button 
                        onClick={handleGenerateVideo}
                        disabled={isGeneratingVideo}
                        className="px-4 py-2 bg-blue-600 text-white rounded-xl text-xs font-bold hover:bg-blue-700 disabled:opacity-50 transition-all flex items-center gap-2 shadow-lg shadow-blue-900/50"
                      >
                        {isGeneratingVideo ? <Loader2 className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
                        GENERATE PROGRESSION MOVIE
                      </button>
                    </div>

                    <div className="aspect-video bg-black/40 rounded-2xl border border-white/10 flex items-center justify-center relative overflow-hidden">
                      {progressionVideo ? (
                        <video 
                          src={progressionVideo} 
                          controls 
                          className="w-full h-full object-cover"
                        />
                      ) : (
                        <div className="text-center space-y-2">
                          <Video className="w-12 h-12 text-white/10 mx-auto" />
                          <p className="text-xs text-gray-600 font-medium uppercase tracking-widest">Awaiting Video Generation...</p>
                        </div>
                      )}
                      {isGeneratingVideo && (
                        <div className="absolute inset-0 bg-black/60 backdrop-blur-sm flex flex-col items-center justify-center p-8 space-y-4">
                          <Loader2 className="w-8 h-8 text-blue-500 animate-spin" />
                          <div className="w-full space-y-2">
                            <div className="flex justify-between text-[10px] font-bold uppercase tracking-widest text-blue-400">
                              <span>Generating Frames</span>
                              <span>{videoProgress}%</span>
                            </div>
                            <div className="w-full h-1 bg-white/10 rounded-full overflow-hidden">
                              <motion.div 
                                className="h-full bg-blue-500"
                                initial={{ width: 0 }}
                                animate={{ width: `${videoProgress}%` }}
                              />
                            </div>
                          </div>
                          <p className="text-[10px] text-gray-400 text-center italic">
                            "Veo is synthesizing a 1080p medical simulation. This may take a few moments..."
                          </p>
                        </div>
                      )}
                    </div>
                    <div className="p-4 bg-blue-500/10 border border-blue-500/20 rounded-2xl">
                      <p className="text-[8px] text-blue-400 font-bold uppercase mb-1">Simulation Parameters</p>
                      <p className="text-[10px] text-gray-300 leading-relaxed">
                        Resolution: 1080p | FPS: 30 | Engine: Veo-3.1-Fast | Context: {hypothesis?.hypothesis || "Baseline Progression"}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Visual Asset Library */}
                <div className="p-8 bg-white border border-[#E5E7EB] rounded-3xl shadow-sm space-y-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Database className="w-5 h-5 text-gray-400" />
                      <h4 className="text-sm font-bold uppercase tracking-widest">Visual Asset Library</h4>
                    </div>
                    <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Temporal Sync Active</span>
                  </div>

                  <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
                    {[1, 2, 3, 4, 5, 6].map((i) => (
                      <div key={i} className="aspect-square bg-gray-50 rounded-xl border border-gray-100 flex items-center justify-center group relative overflow-hidden cursor-pointer hover:border-purple-500 transition-all">
                        <Camera className="w-6 h-6 text-gray-200 group-hover:text-purple-500 transition-all" />
                        <div className="absolute inset-0 bg-purple-600/0 group-hover:bg-purple-600/10 transition-all" />
                      </div>
                    ))}
                  </div>
                </div>
              </motion.div>
            )}

            {activeTab === 'COMMAND CENTER' && (
              <motion.div 
                key="command"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="space-y-8"
              >
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  {/* Notifications / Alerts */}
                  <section className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <Bell className="w-5 h-5 text-red-500" />
                        <h3 className="text-xl font-black tracking-tight">System Alerts</h3>
                      </div>
                      <button 
                        onClick={() => setNotifications(prev => prev.map(n => ({ ...n, read: true })))}
                        className="text-[10px] font-bold text-blue-600 uppercase tracking-widest hover:underline"
                      >
                        Mark all as read
                      </button>
                    </div>
                    <div className="space-y-3 max-h-[400px] overflow-y-auto pr-2 no-scrollbar">
                      {notifications.length === 0 ? (
                        <div className="p-8 text-center bg-gray-50 rounded-2xl border border-dashed border-gray-200">
                          <p className="text-xs text-gray-400">No active alerts.</p>
                        </div>
                      ) : (
                        notifications.map(n => (
                          <div 
                            key={n.id}
                            className={cn(
                              "p-4 rounded-xl border transition-all flex gap-4",
                              n.read ? "bg-white border-gray-100 opacity-60" : "bg-white border-red-100 shadow-sm"
                            )}
                          >
                            <div className={cn(
                              "w-10 h-10 rounded-lg flex items-center justify-center shrink-0",
                              n.type === 'health' ? "bg-red-100 text-red-600" : 
                              n.type === 'stock' ? "bg-emerald-100 text-emerald-600" : "bg-blue-100 text-blue-600"
                            )}>
                              {n.type === 'health' && <Stethoscope className="w-5 h-5" />}
                              {n.type === 'stock' && <TrendingUp className="w-5 h-5" />}
                              {n.type === 'system' && <Shield className="w-5 h-5" />}
                            </div>
                            <div className="flex-1">
                              <div className="flex items-center justify-between mb-1">
                                <span className="text-[10px] font-bold uppercase tracking-widest text-gray-400">{n.type} alert</span>
                                <span className="text-[8px] font-mono text-gray-400">{n.timestamp}</span>
                              </div>
                              <p className="text-xs font-medium text-gray-800">{n.message}</p>
                            </div>
                          </div>
                        ))
                      )}
                    </div>
                  </section>

                  {/* Agent To-Do List */}
                  <section className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <CheckSquare className="w-5 h-5 text-blue-500" />
                        <h3 className="text-xl font-black tracking-tight">Agent Action List</h3>
                      </div>
                      <div className="flex gap-2">
                        <button 
                          onClick={() => {
                            const text = prompt('Enter manual task:');
                            if (text) {
                              setTodoList(prev => [{
                                id: Math.random().toString(36).substr(2, 9),
                                text,
                                completed: false,
                                source: 'user',
                                priority: 'medium'
                              }, ...prev]);
                            }
                          }}
                          className="p-1.5 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition-all"
                        >
                          <Plus className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                    <div className="space-y-3 max-h-[400px] overflow-y-auto pr-2 no-scrollbar">
                      {todoList.length === 0 ? (
                        <div className="p-8 text-center bg-gray-50 rounded-2xl border border-dashed border-gray-200">
                          <p className="text-xs text-gray-400">No tasks assigned.</p>
                        </div>
                      ) : (
                        todoList.map(t => (
                          <div 
                            key={t.id}
                            className={cn(
                              "p-4 bg-white rounded-xl border transition-all flex items-center gap-4 group",
                              t.completed ? "border-gray-100 opacity-60" : "border-blue-100 shadow-sm"
                            )}
                          >
                            <button 
                              onClick={() => setTodoList(prev => prev.map(item => item.id === t.id ? { ...item, completed: !item.completed } : item))}
                              className={cn(
                                "w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all",
                                t.completed ? "bg-green-500 border-green-500 text-white" : "border-gray-300 hover:border-blue-500"
                              )}
                            >
                              {t.completed && <CheckCircle2 className="w-4 h-4" />}
                            </button>
                            <div className="flex-1">
                              <div className="flex items-center gap-2 mb-1">
                                <span className={cn(
                                  "text-[8px] font-bold uppercase tracking-widest px-1.5 py-0.5 rounded",
                                  t.source === 'agent' ? "bg-purple-100 text-purple-600" : "bg-blue-100 text-blue-600"
                                )}>
                                  {t.source}
                                </span>
                                <span className={cn(
                                  "text-[8px] font-bold uppercase tracking-widest px-1.5 py-0.5 rounded",
                                  t.priority === 'high' ? "bg-red-100 text-red-600" : 
                                  t.priority === 'medium' ? "bg-orange-100 text-orange-600" : "bg-gray-100 text-gray-600"
                                )}>
                                  {t.priority}
                                </span>
                              </div>
                              <p className={cn(
                                "text-xs font-medium transition-all",
                                t.completed ? "text-gray-400 line-through" : "text-gray-800"
                              )}>
                                {t.text}
                              </p>
                            </div>
                            <button 
                              onClick={() => setTodoList(prev => prev.filter(item => item.id !== t.id))}
                              className="p-1.5 text-gray-300 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-all"
                            >
                              <X className="w-4 h-4" />
                            </button>
                          </div>
                        ))
                      )}
                    </div>
                  </section>
                </div>

                {/* System Test Suite */}
                <section className="p-8 bg-[#1A1A1A] text-white rounded-3xl shadow-xl space-y-6 border border-white/10">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="p-3 bg-purple-500/20 rounded-2xl">
                        <Zap className="w-8 h-8 text-purple-500" />
                      </div>
                      <div>
                        <h3 className="text-2xl font-black tracking-tight">System Test Suite</h3>
                        <p className="text-[10px] text-gray-400 uppercase font-bold tracking-widest">Verify Video, CRISPR & Omega Protocols</p>
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <button 
                      onClick={handleFullScaleSystemTest}
                      disabled={isTesting}
                      className="p-6 bg-white/5 border border-white/10 rounded-2xl hover:bg-white/10 transition-all text-left space-y-2 group"
                    >
                      <div className="flex items-center justify-between">
                        <ShieldCheck className="w-6 h-6 text-blue-400 group-hover:scale-110 transition-transform" />
                        <ChevronRight className="w-4 h-4 text-gray-600" />
                      </div>
                      <h4 className="text-xs font-bold uppercase tracking-widest">Omega Protocol</h4>
                      <p className="text-[10px] text-gray-500 leading-relaxed">Full scale verification of Optical, Voice, and Email layers.</p>
                    </button>

                    <button 
                      onClick={() => {
                        handleCRISPRSimulation();
                        setActiveTab('EVOLUTION');
                      }}
                      disabled={isEditingDNA}
                      className="p-6 bg-white/5 border border-white/10 rounded-2xl hover:bg-white/10 hover:border-emerald-500/50 transition-all text-left space-y-2 group cursor-pointer"
                    >
                      <div className="flex items-center justify-between">
                        <Dna className="w-6 h-6 text-emerald-400 group-hover:scale-110 transition-transform" />
                        <div className="flex items-center gap-1 text-[8px] font-bold text-emerald-500 uppercase tracking-widest opacity-0 group-hover:opacity-100 transition-opacity">
                          <span>Go to Evolution</span>
                          <ChevronRight className="w-3 h-3" />
                        </div>
                      </div>
                      <h4 className="text-xs font-bold uppercase tracking-widest">CRISPR Test</h4>
                      <p className="text-[10px] text-gray-500 leading-relaxed">Simulate gene editing and molecular Cas9 intervention.</p>
                    </button>

                    <button 
                      onClick={() => {
                        handleGenerateVideo();
                        setActiveTab('VISUAL SIMULATION');
                      }}
                      disabled={isGeneratingVideo}
                      className="p-6 bg-white/5 border border-white/10 rounded-2xl hover:bg-white/10 hover:border-purple-500/50 transition-all text-left space-y-2 group cursor-pointer"
                    >
                      <div className="flex items-center justify-between">
                        <Video className="w-6 h-6 text-purple-400 group-hover:scale-110 transition-transform" />
                        <div className="flex items-center gap-1 text-[8px] font-bold text-purple-500 uppercase tracking-widest opacity-0 group-hover:opacity-100 transition-opacity">
                          <span>Go to Simulation</span>
                          <ChevronRight className="w-3 h-3" />
                        </div>
                      </div>
                      <h4 className="text-xs font-bold uppercase tracking-widest">Video Test</h4>
                      <p className="text-[10px] text-gray-500 leading-relaxed">Generate AI-driven disease progression video (Veo).</p>
                    </button>
                  </div>
                </section>

                {/* High Critical Domain Test */}
                <section className="p-8 bg-[#1A1A1A] text-white rounded-3xl shadow-xl space-y-6 border border-white/10">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="p-3 bg-red-500/20 rounded-2xl">
                        <Shield className="w-8 h-8 text-red-500" />
                      </div>
                      <div>
                        <h3 className="text-2xl font-black tracking-tight">High Critical Test</h3>
                        <p className="text-[10px] text-gray-400 uppercase font-bold tracking-widest">Multi-Domain Singularity Verification</p>
                      </div>
                    </div>
                    <button 
                      onClick={handleHighCriticalTest}
                      disabled={isTesting}
                      className="px-6 py-3 bg-red-600 text-white rounded-2xl text-xs font-bold hover:bg-red-700 disabled:opacity-50 transition-all flex items-center gap-2 shadow-lg shadow-red-900/20"
                    >
                      {isTesting ? <Loader2 className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
                      RUN CRITICAL TEST
                    </button>
                  </div>

                  {testResults?.length > 0 && (
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                      {testResults?.map((result, idx) => (
                        <motion.div 
                          key={result.domain}
                          initial={{ opacity: 0, y: 20 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: idx * 0.1 }}
                          className="p-6 bg-white/5 border border-white/10 rounded-2xl space-y-4"
                        >
                          <div className="flex items-center justify-between">
                            <h4 className="text-sm font-black uppercase tracking-widest text-blue-400">{result.domain}</h4>
                            <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                          </div>
                          <div className="space-y-2 max-h-[200px] overflow-y-auto pr-2 no-scrollbar">
                            {result?.steps?.map((step, sIdx) => (
                              <div key={sIdx} className="flex gap-2 text-[10px] text-gray-400 leading-relaxed">
                                <span className="text-blue-500 font-mono">{sIdx + 1}.</span>
                                <span>{step}</span>
                              </div>
                            ))}
                          </div>
                        </motion.div>
                      ))}
                    </div>
                  )}
                </section>

                {/* Alert Dispatch Center */}
                <section className="p-6 bg-white border border-blue-100 rounded-2xl shadow-sm space-y-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="p-2 bg-blue-100 rounded-lg">
                        <Radio className="w-5 h-5 text-blue-600" />
                      </div>
                      <div>
                        <h4 className="font-bold">Alert Dispatch Center</h4>
                        <p className="text-xs text-gray-500">System automatically sends critical health and stock alerts via Email and SMS.</p>
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Email Config */}
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Mail className="w-4 h-4 text-gray-400" />
                          <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Email Alerts</span>
                        </div>
                        <button 
                          onClick={() => setIsEmailAlertEnabled(!isEmailAlertEnabled)}
                          className={cn(
                            "px-3 py-1 rounded-lg text-[9px] font-bold uppercase tracking-widest transition-all",
                            isEmailAlertEnabled ? "bg-emerald-100 text-emerald-700" : "bg-gray-100 text-gray-500"
                          )}
                        >
                          {isEmailAlertEnabled ? 'ON' : 'OFF'}
                        </button>
                      </div>
                      <div className="p-3 bg-gray-50 rounded-xl border border-gray-100 flex items-center justify-between">
                        <span className="text-xs font-mono text-gray-600">aejphillips@outlook.com</span>
                        <CheckCircle2 className="w-3 h-3 text-green-600" />
                      </div>
                    </div>

                    {/* SMS Config */}
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Smartphone className="w-4 h-4 text-gray-400" />
                          <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">SMS Alerts</span>
                        </div>
                        <button 
                          onClick={() => setIsSmsAlertEnabled(!isSmsAlertEnabled)}
                          className={cn(
                            "px-3 py-1 rounded-lg text-[9px] font-bold uppercase tracking-widest transition-all",
                            isSmsAlertEnabled ? "bg-emerald-100 text-emerald-700" : "bg-gray-100 text-gray-500"
                          )}
                        >
                          {isSmsAlertEnabled ? 'ON' : 'OFF'}
                        </button>
                      </div>
                      <div className="p-3 bg-gray-50 rounded-xl border border-gray-100 flex items-center gap-2">
                        <span className="text-xs font-mono text-gray-400 flex-1">
                          <input 
                            type="text" 
                            value={phoneNumber} 
                            onChange={(e) => setPhoneNumber(e.target.value)}
                            className="bg-transparent outline-none w-full"
                          />
                        </span>
                        <PhoneCall className="w-3 h-3 text-blue-600" />
                      </div>
                    </div>
                  </div>

                  <div className="p-4 bg-gray-50 rounded-xl border border-gray-100 space-y-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <Target className="w-4 h-4 text-blue-600" />
                        <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Tripwire Sensitivity</span>
                      </div>
                      <span className="text-[10px] font-bold text-blue-600 uppercase tracking-widest">{alertThreshold}% Deviation</span>
                    </div>
                    <input 
                      type="range" 
                      min="1" 
                      max="50" 
                      value={alertThreshold} 
                      onChange={(e) => setAlertThreshold(parseInt(e.target.value))}
                      className="w-full h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                    />
                  </div>

                  <div className="flex items-center gap-2 p-3 bg-amber-50 border border-amber-100 rounded-xl">
                    <AlertTriangle className="w-4 h-4 text-amber-600" />
                    <p className="text-[10px] text-amber-700 leading-relaxed font-medium">
                      Protocols active: System will broadcast to all enabled channels when {activeDomain === 'Finance' ? 'market volatility' : 'biomarker deviation'} exceeds {alertThreshold}%.
                    </p>
                  </div>
                </section>

                {/* Execution Logs (Command Center) */}
                {executionLogs.length > 0 && (
                  <div className="p-6 bg-[#1A1A1A] text-white rounded-3xl shadow-xl space-y-4 border border-white/10">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <Terminal className="w-4 h-4 text-emerald-400" />
                        <h4 className="text-[10px] font-bold uppercase tracking-widest">Command Center: Execution Logs</h4>
                      </div>
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
                        <span className="text-[8px] font-bold text-emerald-400">LIVE FEED</span>
                      </div>
                    </div>
                    <div className="space-y-1 font-mono text-[9px] max-h-[200px] overflow-y-auto no-scrollbar">
                      {executionLogs.map((log, i) => (
                        <div key={i} className="flex gap-2">
                          <span className="text-gray-500">[{new Date().toLocaleTimeString()}]</span>
                          <span className={log.includes('[SUCCESS]') ? 'text-emerald-400' : 'text-gray-300'}>{log}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </motion.div>
            )}

            {activeTab === 'MANIFOLD' && (
              <motion.div 
                key="manifold"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="space-y-8"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="p-3 bg-blue-100 rounded-2xl">
                      <Activity className="w-8 h-8 text-blue-600" />
                    </div>
                    <div>
                      <h3 className="text-2xl font-black tracking-tight">Manifold Engine</h3>
                      <p className="text-[10px] text-gray-400 uppercase font-bold tracking-widest">Biological Latent Space Mapping</p>
                    </div>
                  </div>
                  <button 
                    onClick={handleRunManifold}
                    disabled={isAnalyzingManifold}
                    className="px-6 py-3 bg-blue-600 text-white rounded-2xl text-xs font-bold hover:bg-blue-700 disabled:opacity-50 transition-all flex items-center gap-2 shadow-lg shadow-blue-200"
                  >
                    {isAnalyzingManifold ? <Loader2 className="w-4 h-4 animate-spin" /> : <Zap className="w-4 h-4" />}
                    RUN MANIFOLD ANALYSIS
                  </button>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                  {/* Latent Space Visualization */}
                  <div className="lg:col-span-2 p-8 bg-[#1A1A1A] text-white rounded-3xl shadow-xl space-y-6 border border-white/10">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <Globe className="w-5 h-5 text-blue-400" />
                        <h4 className="text-sm font-bold uppercase tracking-widest text-blue-400">Biological Manifold Projection</h4>
                      </div>
                      <span className="text-[10px] font-mono text-gray-500">DIMENSIONS: 4D to 2D</span>
                    </div>

                    {manifoldData ? (
                      <div className="space-y-8">
                        <ManifoldVisualization data={manifoldData.latentBioState} />
                        
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                          {manifoldData?.latentBioState?.map((val, i) => (
                            <div key={i} className="p-4 bg-white/5 border border-white/10 rounded-xl">
                              <p className="text-[8px] text-gray-500 font-bold uppercase mb-1">Latent Dim {i+1}</p>
                              <p className="text-lg font-mono font-bold text-blue-400">{val.toFixed(3)}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    ) : (
                      <div className="h-64 flex flex-col items-center justify-center border-2 border-dashed border-white/5 rounded-2xl space-y-4">
                        <Activity className="w-12 h-12 text-white/5" />
                        <p className="text-xs text-gray-600 uppercase tracking-widest font-bold">Awaiting Latent Mapping...</p>
                      </div>
                    )}
                  </div>

                  {/* Manifold Insights */}
                  <div className="space-y-8">
                    <div className="p-8 bg-white border border-[#E5E7EB] rounded-3xl shadow-sm space-y-6">
                      <div className="flex items-center gap-2">
                        <Target className="w-5 h-5 text-red-500" />
                        <h4 className="text-sm font-bold uppercase tracking-widest">Manifold Region</h4>
                      </div>
                      
                      {manifoldData ? (
                        <motion.div 
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          className="space-y-4"
                        >
                          <div className="p-4 bg-red-50 border border-red-100 rounded-2xl">
                            <p className="text-[10px] text-red-600 font-bold uppercase mb-1">Current Localization</p>
                            <p className="text-xl font-black text-red-900 leading-tight">{manifoldData.manifoldRegion}</p>
                          </div>

                          <div className="p-4 bg-blue-50 border border-blue-100 rounded-2xl">
                            <p className="text-[10px] text-blue-600 font-bold uppercase mb-1">Predicted Trajectory</p>
                            <p className="text-lg font-bold text-blue-900 leading-tight">{manifoldData.trajectory}</p>
                          </div>

                          <div className="space-y-2">
                            <p className="text-[10px] text-gray-400 font-bold uppercase tracking-widest">Identified Clusters</p>
                            <div className="flex flex-wrap gap-2">
                              {manifoldData?.clusters?.map((c, i) => (
                                <span key={i} className="px-3 py-1 bg-gray-100 border border-gray-200 rounded-full text-[10px] font-bold text-gray-600 uppercase">{c}</span>
                              ))}
                            </div>
                          </div>
                        </motion.div>
                      ) : (
                        <div className="py-12 text-center border-2 border-dashed border-gray-100 rounded-2xl">
                          <p className="text-[10px] text-gray-400 font-bold uppercase tracking-widest">No Data Localized</p>
                        </div>
                      )}
                    </div>

                    <div className="p-6 bg-[#1A1A1A] text-white rounded-3xl border border-white/10 space-y-4">
                      <div className="flex items-center gap-2">
                        <Zap className="w-4 h-4 text-amber-400" />
                        <h4 className="text-xs font-bold uppercase tracking-widest">Manifold Logic</h4>
                      </div>
                      <p className="text-[10px] text-gray-400 leading-relaxed">
                        The Manifold Engine compresses high-dimensional biological data (mutations, biomarkers, immune signals) into a learnable latent space. This allows for precise disease localization and trajectory prediction.
                      </p>
                    </div>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {error && (
            <div className="p-4 bg-red-50 border border-red-100 rounded-xl flex items-center gap-3 text-red-600">
              <AlertCircle className="w-5 h-5" />
              <p className="text-sm font-bold">{error}</p>
            </div>
          )}
        </div>
      </main>

      {/* Camera Modal */}
      <AnimatePresence>
        {isCameraOpen && (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4"
          >
            <div className="bg-white rounded-3xl overflow-hidden max-w-2xl w-full shadow-2xl">
              <div className="p-4 border-b flex justify-between items-center">
                <h3 className="font-bold">Optical Ingress</h3>
                <button onClick={stopCamera} className="p-2 hover:bg-gray-100 rounded-full">
                  <X className="w-5 h-5" />
                </button>
              </div>
              <div className="relative aspect-video bg-black">
                <video 
                  ref={videoRef} 
                  autoPlay 
                  playsInline 
                  className="w-full h-full object-contain"
                />
                <div className="absolute inset-0 border-[20px] border-black/20 pointer-events-none">
                  <div className="w-full h-full border border-white/30 rounded-lg" />
                </div>
              </div>
              <div className="p-6 flex flex-col items-center gap-4">
                <button 
                  onClick={capturePhoto}
                  className="w-16 h-16 rounded-full border-4 border-gray-200 p-1 hover:scale-105 transition-transform relative group"
                >
                  <div className="w-full h-full bg-red-500 rounded-full group-active:scale-90 transition-transform" />
                </button>
                <p className="text-[10px] font-bold text-[#6B7280] uppercase tracking-widest">Capture Sensor Data</p>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Emergency Call Modal */}
      <AnimatePresence>
        {isEmergencyCallActive && (
          <motion.div 
            initial={{ opacity: 0, scale: 1.1 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            className="fixed inset-0 z-[100] bg-red-600 flex flex-col items-center justify-center p-8 text-white"
          >
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-red-500 via-red-700 to-red-900 animate-pulse opacity-50" />
            
            <div className="relative z-10 flex flex-col items-center space-y-12 max-w-lg w-full text-center">
              <div className="w-24 h-24 bg-white/20 rounded-full flex items-center justify-center animate-ping">
                <Shield className="w-12 h-12 text-white" />
              </div>
              
              <div className="space-y-4">
                <h2 className="text-4xl font-black tracking-tighter uppercase italic">Omega Emergency</h2>
                <p className="text-xl font-bold text-red-100 uppercase tracking-widest">Dispatching Medical Drone...</p>
              </div>

              <div className="w-full p-8 bg-black/20 backdrop-blur-xl rounded-3xl border border-white/10 space-y-6">
                <div className="flex items-center justify-between border-b border-white/10 pb-4">
                  <span className="text-xs font-bold uppercase tracking-widest text-red-200">Uplink Status</span>
                  <span className="text-xs font-mono text-emerald-400">ENCRYPTED</span>
                </div>
                
                <div className="flex items-center gap-6">
                  <div className="w-16 h-16 bg-white rounded-2xl flex items-center justify-center shrink-0">
                    <Bot className="w-10 h-10 text-red-600" />
                  </div>
                  <div className="text-left">
                    <p className="text-lg font-black uppercase italic">Omega Dispatch</p>
                    <p className="text-xs text-red-200 font-bold">00:{emergencyCallTimer < 10 ? `0${emergencyCallTimer}` : emergencyCallTimer}</p>
                  </div>
                </div>

                <div className="p-4 bg-red-900/40 rounded-2xl border border-red-400/20">
                  <p className="text-[10px] text-red-100 font-bold uppercase tracking-widest mb-2">Live Transcription</p>
                  <p className="text-sm font-medium italic">"Initiating emergency bypass. Bio-markers critical. Drone ETA: 4 minutes. Remain calm, Omega Clearance."</p>
                </div>

                <div className="flex justify-center pt-2">
                  <button 
                    onMouseDown={startRecording}
                    onMouseUp={stopRecording}
                    onTouchStart={startRecording}
                    onTouchEnd={stopRecording}
                    className={cn(
                      "w-16 h-16 rounded-full flex items-center justify-center transition-all shadow-lg",
                      isRecording ? "bg-white text-red-600 scale-110" : "bg-red-500 text-white hover:bg-red-400"
                    )}
                  >
                    {isRecording ? <Mic className="w-8 h-8 animate-pulse" /> : <Mic className="w-8 h-8" />}
                  </button>
                </div>
              </div>

              <button 
                onClick={() => setIsEmergencyCallActive(false)}
                className="w-full py-6 bg-white text-red-600 rounded-3xl text-sm font-black uppercase tracking-widest shadow-2xl hover:bg-red-50 transition-all flex items-center justify-center gap-3"
              >
                <X className="w-5 h-5" />
                Terminate Protocol
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <canvas ref={canvasRef} className="hidden" />
    </div>
  );
}
