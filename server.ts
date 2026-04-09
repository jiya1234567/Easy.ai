import express from "express";
import { createServer as createViteServer } from "vite";
import path from "path";
import archiver from "archiver";
import fs from "fs";

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
