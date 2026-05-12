import express from "express";
import { createServer as createViteServer } from "vite";
import path from "path";
import archiver from "archiver";
import fs from "fs";
import { exec } from "child_process";
import { BigQuery } from "@google-cloud/bigquery";
import dotenv from "dotenv";

dotenv.config();

let bigquery: BigQuery | null = null;
try {
  const keyBlob = process.env.GOOGLE_CLOUD_PRIVATE_KEY;
  const project = process.env.GOOGLE_CLOUD_PROJECT;
  const clientEmail = process.env.GOOGLE_CLOUD_CLIENT_EMAIL;

  if (keyBlob) {
    if (keyBlob.trim().startsWith('{')) {
      const credentials = JSON.parse(keyBlob);
      bigquery = new BigQuery({
        projectId: credentials.project_id,
        credentials: {
          client_email: credentials.client_email,
          private_key: credentials.private_key,
        },
      });
      console.log("BigQuery initialized with JSON blob from GOOGLE_CLOUD_PRIVATE_KEY");
    } else {
      if (!project || !clientEmail) {
        throw new Error("Missing GOOGLE_CLOUD_PROJECT or GOOGLE_CLOUD_CLIENT_EMAIL when using raw private key.");
      }
      // Ensure newlines are correctly formatted if pasted as a single string
      const formattedKey = keyBlob.replace(/\\n/g, '\n');
      bigquery = new BigQuery({
        projectId: project,
        credentials: {
          client_email: clientEmail,
          private_key: formattedKey,
        },
      });
      console.log("BigQuery initialized with separate variables (Project, Email, Raw Key).");
    }
  } else {
    console.warn("GOOGLE_CLOUD_PRIVATE_KEY not found in .env. BigQuery operations will fail.");
  }
} catch (e: any) {
  console.error("Failed to initialize BigQuery:", e.message);
}

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(express.json());

  // API routes FIRST
  app.get("/api/health", (req, res) => {
    console.log(`[${new Date().toISOString()}] Health check from ${req.ip}`);
    res.json({ status: "ok", message: "Universal Lab Server Operational" });
  });

  app.get("/api/download-backup", (req, res) => {
    const backupPath = path.join(process.cwd(), "python_backup");
    
    if (!fs.existsSync(backupPath)) {
      return res.status(404).json({ error: "Backup directory not found" });
    }

    const archive = archiver("zip", {
      zlib: { level: 9 } // Sets the compression level.
    });

    res.attachment("python_backup.zip");

    archive.on("error", (err) => {
      res.status(500).send({ error: err.message });
    });

    archive.pipe(res);
    archive.directory(backupPath, false);
    archive.finalize();
  });

  app.post("/api/alert", (req, res) => {
    const { type, message, email } = req.body;
    console.log(`[ALERT] Sending ${type} email to ${email}: ${message}`);
    // In a real app, integrate with SendGrid/Nodemailer here
    res.json({ status: "sent", timestamp: new Date().toISOString() });
  });

  // BigQuery Endpoints
  app.get("/api/bigquery/verify", async (req, res) => {
    if (!bigquery) {
      return res.status(500).json({ error: "BigQuery client not initialized. Check server credentials." });
    }
    try {
      const query = `SELECT 1 as id, 'Connection Test' as status, CURRENT_TIMESTAMP() as time`;
      const [job] = await bigquery.createQueryJob({ query });
      const [rows] = await job.getQueryResults();
      res.json({ status: "success", data: rows[0] });
    } catch (e: any) {
      console.error("BigQuery Verify Error:", e);
      res.status(500).json({ error: e.message });
    }
  });

  app.post("/api/bigquery/persist_health", async (req, res) => {
    if (!bigquery) {
      return res.status(500).json({ error: "BigQuery client not initialized." });
    }
    try {
      // Assuming a dataset 'al' and table 'health_scans' exist.
      // If not, we log the attempt to simulate persistence.
      const scanData = req.body;
      console.log(`[BigQuery] Simulating insertion of health scan data:`, scanData);
      
      // Real insert logic (commented out to prevent errors if table doesn't exist yet):
      // await bigquery.dataset("al").table("health_scans").insert([scanData]);

      res.json({ status: "success", message: "Health scan persisted to BigQuery (simulated)", data: scanData });
    } catch (e: any) {
      console.error("BigQuery Persist Error:", e);
      res.status(500).json({ error: e.message });
    }
  });

  app.post("/api/orchestrate", (req, res) => {
    const { domain, ingress_data } = req.body;
    console.log(`[ORCHESTRATOR] Initiating 9-step loop for domain: ${domain}`);

    const pythonScript = path.join(process.cwd(), "intelligence", "orchestrator_engine.py");
    const command = `py "${pythonScript}" "${domain}"`;

    exec(command, (error, stdout, stderr) => {
      if (error) {
        console.error(`[ORCHESTRATOR ERROR]: ${error.message}`);
        return res.status(500).json({ error: error.message });
      }
      if (stderr) {
        console.warn(`[ORCHESTRATOR STDERR]: ${stderr}`);
      }

      try {
        const result = JSON.parse(stdout);
        res.json(result);
      } catch (parseError) {
        console.error(`[ORCHESTRATOR PARSE ERROR]: ${stdout}`);
        res.status(500).json({ error: "Failed to parse orchestrator output" });
      }
    });
  });

  // Vite middleware for development
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), 'dist');
    app.use(express.static(distPath));
    app.get('*', (req, res) => {
      res.sendFile(path.join(distPath, 'index.html'));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on http://localhost:${PORT}`);
  });
}

startServer();
