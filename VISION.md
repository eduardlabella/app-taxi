# VISION.md  
*A 2–3 year roadmap for the Taxi Data Platform*

---

## Summary  
Our current PoC already **collects, processes and analyses** ride events, and **returns** up‑to‑date tariffs & hot‑spots to each car via API Management → Azure Functions → Event Hub / Web PubSub.  
Over the next 24–36 months, we will evolve the platform around **three strategic pillars**:

| Pillar | Core Goal | Key Outcomes |
|--------|-----------|--------------|
| **1 · Architectural Evolution** | Fully device‑aware, zero‑trust, real‑time messaging | <br>• Replace Web PubSub + Event Hub with **Azure IoT Hub** for unified D2C & C2D<br>• Microsoft Sentinel + Defender for Cloud<br>• Multi‑region fail‑over (active/active) |
| **2 · AI‑Driven Analytics** | Autonomous, multi‑agent decision loop | <br>• Deploy **FraudAgent, PricingAgent, HotspotAgent**<br>• Agents exchange context via **MCP‑v1 (Model Context Protocol)** messages on Event Hub<br>• Databricks / Synapse MLflow for continuous re‑training<br>
| **3 · Commercial & Vertical Expansion** | Productise the platform for third‑party fleets | <br>• Offer a white‑label “Mobility Data Platform” for food‑delivery, logistics, ride‑share<br>• Add tenancy & billing modules<br>• Publish selected live metrics via secure APIs / Data Marketplace |

---