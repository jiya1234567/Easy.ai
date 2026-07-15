"""
OMEGA-CORE | World Model Visualizer
===================================
Generates high-fidelity visual simulations and interactive 3D scenes for the 
scientific and robotics dashboards.
"""

import io
import math
import base64
import numpy as np
from PIL import Image, ImageDraw

class WorldModelVisualizer:
    @staticmethod
    def generate_3d_plotly_scene(spatial_engine, path_result=None):
        """
        Generates an interactive 3D Plotly Figure showing:
          - Mapped obstacles (as red 3D spheres/markers)
          - Scene graph nodes (as green 3D spheres/markers with labels)
          - Start/Goal positions
          - The planned trajectory (as a 3D line)
        """
        import plotly.graph_objects as go
        fig = go.Figure()

        # 1. Plot Obstacles
        obs_x, obs_y, obs_z, obs_text = [], [], [], []
        for obs in spatial_engine.active_obstacles:
            obs_x.append(obs.center.x)
            obs_y.append(obs.center.y)
            obs_z.append(obs.center.z)
            obs_text.append(f"Obstacle: {obs.semantic_label} (ID: {obs.obstacle_id}, Severity: {obs.severity})")

        if obs_x:
            fig.add_trace(go.Scatter3d(
                x=obs_x, y=obs_y, z=obs_z,
                mode="markers",
                marker=dict(size=8, color="#ef4444", symbol="diamond", opacity=0.8),
                text=obs_text,
                name="Obstacles"
            ))

        # 2. Plot Scene Graph Nodes
        sg_x, sg_y, sg_z, sg_text = [], [], [], []
        for node in spatial_engine.scene_graph.values():
            sg_x.append(node.position.x)
            sg_y.append(node.position.y)
            sg_z.append(node.position.z)
            sg_text.append(f"Entity: {node.label} (ID: {node.node_id})")

        if sg_x:
            fig.add_trace(go.Scatter3d(
                x=sg_x, y=sg_y, z=sg_z,
                mode="markers+text",
                marker=dict(size=6, color="#10b981", symbol="circle"),
                text=sg_text,
                textposition="top center",
                name="Entities"
            ))

        # 3. Plot Path Trajectory
        if path_result and path_result.get("trajectory"):
            traj = path_result["trajectory"]
            px_val = [pt["x"] for pt in traj]
            py_val = [pt["y"] for pt in traj]
            pz_val = [pt["z"] for pt in traj]

            fig.add_trace(go.Scatter3d(
                x=px_val, y=py_val, z=pz_val,
                mode="lines+markers",
                line=dict(color="#38bdf8", width=4),
                marker=dict(size=4, color="#0284c7"),
                name="Trajectory"
            ))

            # Start and Goal
            fig.add_trace(go.Scatter3d(
                x=[px_val[0]], y=[py_val[0]], z=[pz_val[0]],
                mode="markers",
                marker=dict(size=10, color="#22c55e", symbol="square"),
                name="Start"
            ))
            fig.add_trace(go.Scatter3d(
                x=[px_val[-1]], y=[py_val[-1]], z=[pz_val[-1]],
                mode="markers",
                marker=dict(size=10, color="#a855f7", symbol="circle"),
                name="Goal"
            ))

        fig.update_layout(
            scene=dict(
                xaxis=dict(title="X (m)", backgroundcolor="#050505", gridcolor="#222", showbackground=True),
                yaxis=dict(title="Y (m)", backgroundcolor="#050505", gridcolor="#222", showbackground=True),
                zaxis=dict(title="Z (m)", backgroundcolor="#050505", gridcolor="#222", showbackground=True),
                aspectmode="manual",
                aspectratio=dict(x=1, y=1, z=0.5)
            ),
            plot_bgcolor="#050505",
            paper_bgcolor="#0d1117",
            font=dict(color="#E2E8F0"),
            height=400,
            margin=dict(l=0, r=0, b=0, t=30)
        )
        return fig

    @staticmethod
    def generate_trajectory_video_gif(spatial_engine, path_result) -> bytes:
        """
        Creates an animated radar-style simulation showing the robot/drone
        traversing the A* path through the obstacles and entities.
        Returns the GIF bytes.
        """
        if not path_result or not path_result.get("trajectory"):
            # Return a default empty canvas GIF
            img = Image.new("RGB", (600, 400), "#0d1117")
            buf = io.BytesIO()
            img.save(buf, format="GIF")
            return buf.getvalue()

        trajectory = path_result["trajectory"]
        obstacles = spatial_engine.active_obstacles
        entities = list(spatial_engine.scene_graph.values())

        frames = []
        n_steps = len(trajectory)

        # Scale factor to map world coordinates [-10, 10] to screen pixels [50, 550]
        def world_to_screen(x, y):
            screen_x = int(300 + x * 25)
            screen_y = int(200 - y * 25) # Invert Y for screen coords
            return screen_x, screen_y

        for step_idx in range(n_steps):
            # Create premium canvas
            img = Image.new("RGB", (600, 400), "#0d1117")
            draw = ImageDraw.Draw(img)

            # Draw fine radar grid
            for r in range(50, 300, 50):
                draw.ellipse([300 - r, 200 - r, 300 + r, 200 + r], outline="#1e293b", width=1)
            draw.line([300, 20, 300, 380], fill="#1e293b", width=1)
            draw.line([20, 200, 580, 200], fill="#1e293b", width=1)

            # Draw static path trajectory (faint blue)
            for i in range(len(trajectory) - 1):
                p1_x, p1_y = world_to_screen(trajectory[i]["x"], trajectory[i]["y"])
                p2_x, p2_y = world_to_screen(trajectory[i+1]["x"], trajectory[i+1]["y"])
                draw.line([p1_x, p1_y, p2_x, p2_y], fill="#1e40af", width=2)

            # Draw Obstacles (Red halos)
            for obs in obstacles:
                ox, oy = world_to_screen(obs.center.x, obs.center.y)
                radius_px = int(obs.radius * 25)
                # Outer pulse
                pulse_color = "#450a0a" if obs.severity == "CRITICAL" else "#310d0d"
                draw.ellipse([ox - radius_px - 8, oy - radius_px - 8, ox + radius_px + 8, oy + radius_px + 8], fill=pulse_color)
                # Obstacle core
                draw.ellipse([ox - radius_px, oy - radius_px, ox + radius_px, oy + radius_px], fill="#ef4444", outline="#f87171", width=1)

            # Draw Entities (Green dots)
            for ent in entities:
                ex, ey = world_to_screen(ent.position.x, ent.position.y)
                draw.ellipse([ex - 6, ey - 6, ex + 6, ey + 6], fill="#10b981", outline="#6ee7b7", width=1)

            # Draw Current Robot Position (Cyan pulse)
            curr_pos = trajectory[step_idx]
            rx, ry = world_to_screen(curr_pos["x"], curr_pos["y"])
            # Pulse ring
            draw.ellipse([rx - 12, ry - 12, rx + 12, ry + 12], outline="#38bdf8", width=2)
            # Robot core
            draw.ellipse([rx - 6, ry - 6, rx + 6, ry + 6], fill="#0ea5e9", outline="#e0f2fe", width=2)

            # Draw HUD Overlays (Scientific labels)
            draw.text((15, 15), "SYSTEM: OMEGA-STAGE-12-SPATIAL-AI", fill="#64748b")
            draw.text((15, 30), f"TELEMETRY: ACTIVE PIPELINE TARGET", fill="#64748b")
            draw.text((15, 55), f"ROBOT X: {curr_pos['x']:.2f} m", fill="#38bdf8")
            draw.text((15, 70), f"ROBOT Y: {curr_pos['y']:.2f} m", fill="#38bdf8")
            draw.text((15, 85), f"ROBOT Z: {curr_pos['z']:.2f} m", fill="#38bdf8")
            
            # Bottom info
            draw.text((15, 350), f"TRAJECTORY PROGRESS: {int((step_idx+1)/n_steps*100)}%", fill="#10b981")
            draw.text((15, 365), f"SAFETY SCORE: {path_result.get('safety_score', 1.0)*100:.0f}%", fill="#10b981")
            
            # Draw coordinate axes indicators
            draw.text((540, 20), "+Y (North)", fill="#475569")
            draw.text((540, 365), "+X (East)", fill="#475569")

            frames.append(img)

        # Save to animated GIF bytes
        buf = io.BytesIO()
        frames[0].save(
            buf,
            format="GIF",
            save_all=True,
            append_images=frames[1:],
            duration=120, # ms per frame
            loop=0
        )
        return buf.getvalue()

    @staticmethod
    def generate_disease_progression_gif() -> bytes:
        """
        Simulates biophysical disease cell progression and CRISPR knock-out intervention.
        Five stages representing a cellular environment under attack, then rescued.
        Returns the GIF bytes.
        """
        width, height = 600, 400
        frames = []

        # Generate a seed set of 30 cell coordinates representing healthy cells in a cluster
        np.random.seed(42)
        cell_coords = []
        for _ in range(35):
            r = np.random.uniform(10, 110)
            theta = np.random.uniform(0, 2 * math.pi)
            cx = 300 + r * math.cos(theta)
            cy = 180 + r * math.sin(theta)
            cell_coords.append((cx, cy))

        stages = [
            {"name": "STAGE 1: HEALTHY HOMEOSTASIS", "desc": "Normal cell metabolic activity. State Tensor Stable.", "cancer_pct": 0.0, "crispr": False},
            {"name": "STAGE 2: ONCOGENIC INITIATION", "desc": "EGFR driver mutation excites cellular division.", "cancer_pct": 0.15, "crispr": False},
            {"name": "STAGE 3: HYPOXIC MUTATION DIVERGENCE", "desc": "Tumor tissue replicates. Oxygen deprivation triggers growth.", "cancer_pct": 0.65, "crispr": False},
            {"name": "STAGE 4: CRISPR DO-INTERVENTION INJECTED", "desc": "CAS9 payload target BRCA1_exon11 active. Cleaving mutation.", "cancer_pct": 0.40, "crispr": True},
            {"name": "STAGE 5: BIOPHYSICAL REGIME SHIFT", "desc": "Malignancy suppressed. Cellular homeostasis restored.", "cancer_pct": 0.02, "crispr": False}
        ]

        # Expand stages to 8 frames per stage for smooth transition
        total_frames = len(stages) * 8
        
        for f_idx in range(total_frames):
            stage_idx = f_idx // 8
            sub_step = f_idx % 8
            stage = stages[stage_idx]
            
            # Create canvas
            img = Image.new("RGB", (width, height), "#050505")
            draw = ImageDraw.Draw(img)

            # Draw background grid
            for x in range(0, width, 40):
                draw.line([x, 0, x, height], fill="#111", width=1)
            for y in range(0, height, 40):
                draw.line([0, y, width, y], fill="#111", width=1)

            # Draw CRISPR payload particles heading in if active
            if stage["crispr"]:
                for i in range(5):
                    # CRISPR payloads move from top-left to center cell cluster
                    progress = (sub_step + 1.0) / 8.0
                    px = int(50 + progress * (250 - 50) + i*15)
                    py = int(50 + progress * (150 - 50) - i*5)
                    # draw cyan payload triangle
                    draw.polygon([px, py - 4, px - 4, py + 4, px + 4, py + 4], fill="#06b6d4")

            # Draw Cells
            for idx, (cx, cy) in enumerate(cell_coords):
                # Determine cell state
                # Cancer probability increases or decreases depending on stage
                # We can stagger the cancer cells based on index
                threshold = stage["cancer_pct"]
                # Interpolate intermediate values for smooth color shift
                if stage_idx < 4:
                    prev_stage = stages[max(0, stage_idx - 1)]
                    interpolated_threshold = prev_stage["cancer_pct"] + (stage["cancer_pct"] - prev_stage["cancer_pct"]) * (sub_step / 8.0)
                else:
                    interpolated_threshold = stage["cancer_pct"]

                is_cancer = (idx / len(cell_coords)) < interpolated_threshold

                # Draw cell body
                size = 14
                if is_cancer:
                    color = "#ef4444"      # Red Cancerous
                    outline = "#f87171"
                    size = 16 + int(math.sin(sub_step) * 2) # Cancer cells pulse and are larger
                else:
                    if stage_idx >= 3 and (idx / len(cell_coords)) < stages[2]["cancer_pct"]:
                        # This cell was cancerous but is now repaired / recovering
                        color = "#10b981"  # Green CRISPR repaired
                        outline = "#a7f3d0"
                    else:
                        color = "#3b82f6"  # Blue Healthy
                        outline = "#60a5fa"

                draw.ellipse([cx - size, cy - size, cx + size, cy + size], fill=color, outline=outline, width=1)
                
                # Draw cell nucleus
                draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill="#020617")

            # Draw HUD / Telemetry info panel
            draw.rectangle([10, 10, 590, 48], fill="#0f172a", outline="#1e293b", width=1)
            draw.text((20, 15), stage["name"], fill="#f8fafc")
            draw.text((20, 30), stage["desc"], fill="#94a3b8")

            # Draw progress bar timeline
            draw.rectangle([15, 375, 585, 385], fill="#0f172a")
            filled_width = int(15 + (f_idx / total_frames) * (585 - 15))
            draw.rectangle([15, 375, filled_width, 385], fill="#2563eb")

            # Metrics
            draw.text((15, 335), f"MUTATED CELLS: {int(interpolated_threshold * len(cell_coords))}/{len(cell_coords)}", fill="#ef4444")
            draw.text((15, 350), f"CRISPR INTENSITY: {98.2 if stage['crispr'] else 0.0}%", fill="#06b6d4")
            
            draw.text((430, 335), f"BIOPHYSICAL COHERENCE: {98.4 - interpolated_threshold * 60:.1f}%", fill="#10b981")
            draw.text((430, 350), f"RULIAD DEPTH: 14,200 Nodes", fill="#64748b")

            frames.append(img)

        # Save to animated GIF bytes
        buf = io.BytesIO()
        frames[0].save(
            buf,
            format="GIF",
            save_all=True,
            append_images=frames[1:],
            duration=150, # ms per frame
            loop=0
        )
        return buf.getvalue()
