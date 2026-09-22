# -*- coding: utf-8 -*-
"""
Builds the complete, professional 20-slide Capstone Defense presentation for NirmalNode.
Authoritative source: NirmalNode Thesis & Project Files.
"""
import os

out_path = r"c:\Users\ASUS\Downloads\capstone 3.2\NirmalNode_Capstone_NEW.html"

# Slide contents list
slides = []

def add_slide(slide_id, tag, title, subtitle, badge, body_html):
    html = f"""
  <div class="slide" id="{slide_id}">
    <div class="slide-header">
      <div>
        <div class="slide-tag">{tag}</div>
        <div class="slide-title">{title}</div>
        <div class="slide-subtitle">{subtitle}</div>
      </div>
      <div class="slide-category-badge">{badge}</div>
    </div>
    <div class="slide-body">
      {body_html}
    </div>
  </div>
"""
    slides.append(html)

print("Defining Slide 1...")
# SLIDE 1: Title Slide (Special full-card layout)
slide_1 = """
  <div class="slide active" id="slide-1" style="padding: 0; border: none; overflow: hidden;">
    <div style="display: flex; height: 100%; width: 100%;">
      <!-- Left Side: Clean Academic Title -->
      <div style="flex: 5.5; padding: 40px 48px; display: flex; flex-direction: column; justify-content: space-between; background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);">
        <div>
          <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 20px;">
            <img src="extracted_figs/uft_logo.png" alt="UFT Logo" style="height: 48px; object-fit: contain;">
            <div>
              <div style="font-size: 13px; font-weight: 800; color: #1e3a8a; letter-spacing: 0.5px; text-transform: uppercase;">University of Frontier Technology, Bangladesh</div>
              <div style="font-size: 11.5px; color: #64748b; font-weight: 500;">Department of Internet of Things and Robotics Engineering</div>
            </div>
          </div>
          
          <div style="display: inline-block; background: #e0f2fe; color: #0369a1; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 4px; letter-spacing: 0.8px; margin-bottom: 12px; text-transform: uppercase;">
            B.Sc. Capstone Defense Presentation
          </div>
          
          <h1 style="font-size: 40px; font-weight: 900; color: #1e3a8a; letter-spacing: -1px; line-height: 1.1; margin-bottom: 12px;">
            NirmalNode
          </h1>
          
          <p style="font-size: 15px; font-weight: 600; color: #0f766e; line-height: 1.45; max-width: 620px; margin-bottom: 18px;">
            Green IoT and Adaptive AI-Assisted Local Air Purification and Pollution Prediction System for Industrial Hotspots in Bangladesh
          </p>
          
          <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 24px;">
            <span style="background: #f1f5f9; border: 1px solid #e2e8f0; color: #334155; font-size: 11.5px; font-weight: 600; padding: 3px 9px; border-radius: 4px;">🎯 Hotspot-Targeted</span>
            <span style="background: #f1f5f9; border: 1px solid #e2e8f0; color: #334155; font-size: 11.5px; font-weight: 600; padding: 3px 9px; border-radius: 4px;">⚡ Green IoT (1.8W)</span>
            <span style="background: #f1f5f9; border: 1px solid #e2e8f0; color: #334155; font-size: 11.5px; font-weight: 600; padding: 3px 9px; border-radius: 4px;">🧠 Incremental AI</span>
            <span style="background: #f1f5f9; border: 1px solid #e2e8f0; color: #334155; font-size: 11.5px; font-weight: 600; padding: 3px 9px; border-radius: 4px;">🛡️ 3-Stage Purification</span>
            <span style="background: #fef08a; border: 1px solid #fde047; color: #854d0e; font-size: 11.5px; font-weight: 700; padding: 3px 9px; border-radius: 4px;">৳ 7,400 / $67</span>
          </div>
        </div>
        
        <div style="border-top: 1.5px solid #e2e8f0; padding-top: 18px; display: flex; justify-content: space-between; align-items: flex-end;">
          <div>
            <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; color: #64748b; letter-spacing: 0.5px; margin-bottom: 4px;">Presented By:</div>
            <div style="font-size: 13.5px; font-weight: 700; color: #1e293b;">Aar Raisatunnesa Hridika</div>
            <div style="font-size: 13.5px; font-weight: 700; color: #1e293b;">Md Rakib Hassan Dipu</div>
            <div style="font-size: 11px; color: #64748b; margin-top: 2px;">Dept. of IoT & Robotics Engineering</div>
          </div>
          
          <div style="text-align: right;">
            <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; color: #64748b; letter-spacing: 0.5px; margin-bottom: 4px;">Supervisor:</div>
            <div style="font-size: 13.5px; font-weight: 700; color: #1e3a8a;">Md. Ashiqussalehin</div>
            <div style="font-size: 11.5px; color: #475569;">Lecturer, Dept. of IoT & Robotics Engineering</div>
            <div style="font-size: 11px; color: #64748b; margin-top: 4px;">September 2026</div>
          </div>
        </div>
      </div>
      
      <!-- Right Side: Real-World Hotspot Visual -->
      <div style="flex: 4.5; position: relative; background: #0f172a; overflow: hidden;">
        <img src="real_world_hotspots.jpg" alt="Industrial Hotspot Bangladesh" style="width: 100%; height: 100%; object-fit: cover; opacity: 0.88;">
        <div style="position: absolute; inset: 0; background: linear-gradient(to top, rgba(15, 23, 42, 0.85) 0%, rgba(15, 23, 42, 0.2) 60%, transparent 100%);"></div>
        <div style="position: absolute; bottom: 24px; left: 24px; right: 24px; color: #ffffff;">
          <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: #38bdf8; margin-bottom: 4px;">Figure 1.1 — Industrial Hotspots in Bangladesh</div>
          <div style="font-size: 12.5px; font-weight: 500; line-height: 1.4; color: #e2e8f0;">
            Direct worker exposure to concentrated metal fumes, combustion gases, and toxic particulates in manufacturing zones.
          </div>
        </div>
      </div>
    </div>
  </div>
"""
slides.append(slide_1)

print("Defining Slide 2...")
# SLIDE 2: The Problem
slide_2_body = """
  <div class="col-half" style="flex: 4.8;">
    <div class="img-frame" style="height: 100%;">
      <img src="real_world_hotspots.jpg" alt="Figure 1.1 Representative Industrial Hotspots" style="width: 100%; height: calc(100% - 24px); object-fit: cover;">
      <div class="img-caption">Figure 1.1: Representative industrial hotspots in Bangladesh (Welding bay fumes & boiler combustion plume)</div>
    </div>
  </div>
  
  <div class="col-half" style="flex: 5.2; justify-content: space-between;">
    <div>
      <div class="callout callout-amber" style="margin-top: 0; margin-bottom: 12px;">
        <strong>The WHO 2021 Reality:</strong> Annual PM2.5 guideline tightened from 10 to <strong>5 μg/m³</strong>. Even the natural background component approaches this limit, leaving near-zero tolerance for industrial emissions (Pai et al., 2022).
      </div>
      
      <div class="bullet-list">
        <div class="bullet-item">
          <div class="bullet-dot"></div>
          <div><strong class="strong-term">Persistent Spatial Hotspots:</strong> Industrial pollution in Bangladesh is not homogeneous across a city—it is concentrated at acute micro-locations (welding bays, boiler rooms, generator bays, chemical stores, loading docks) (Ali et al., 2025; Basak et al., 2025).</div>
        </div>
        <div class="bullet-item">
          <div class="bullet-dot"></div>
          <div><strong class="strong-term">Severe Worker Exposure:</strong> Hotspot workers absorb heavy particulate and gaseous loads—causing lung function impairment (Nasri et al., 2023), construction hazards (Sekhavati et al., 2023), and elevated mental health risks (Alhadhrami et al., 2024).</div>
        </div>
        <div class="bullet-item">
          <div class="bullet-dot"></div>
          <div><strong class="strong-term">Coarse, Impotent Monitoring:</strong> Current municipal monitoring operates at coarse spatial resolution, providing delayed macro reports without local actionable response.</div>
        </div>
        <div class="bullet-item">
          <div class="bullet-dot"></div>
          <div><strong class="strong-term">Plant-Wide Filtration is Infeasible:</strong> Centralized factory HVAC systems cost tens of thousands of dollars—unaffordable for Bangladesh's resource-constrained SME industrial backbone (Chowdhury et al., 2025).</div>
        </div>
      </div>
    </div>
    
    <div class="callout callout-teal">
      <strong>Core Thesis Premise:</strong> If dangerous exposure is localized at specific worker hotspots, air purification must also be <em>localized, pre-emptive, and low-cost</em>—rather than wasting energy attempting to filter entire industrial plants.
    </div>
  </div>
"""
add_slide("slide-2", "1. Problem Motivation", "Why Industrial Air Pollution Needs a Local Solution", "The spatial mismatch between macro-scale monitoring and localized worker exposure", "Background & Context", slide_2_body)

print("Defining Slide 3...")
# SLIDE 3: Where Traditional Approaches Fall Short
slide_3_body = """
  <div style="width: 100%; display: flex; flex-direction: column; justify-content: space-between; height: 100%;">
    <!-- Top 3-Way Flow Comparison -->
    <div style="display: flex; gap: 16px; flex: 1;">
      <!-- Column 1 -->
      <div style="flex: 1; background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 16px; display: flex; flex-direction: column;">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
          <span style="background: #e2e8f0; color: #334155; font-weight: 800; font-size: 11px; padding: 3px 8px; border-radius: 4px;">APPROACH 1</span>
          <h3 style="margin: 0; font-size: 15px; color: #1e3a8a;">Traditional IoT Monitoring</h3>
        </div>
        <div style="font-size: 12.5px; color: #475569; margin-bottom: 12px;">
          Measures ambient pollutants and logs time-series to cloud dashboards or alerts.
        </div>
        <div style="display: flex; flex-direction: column; gap: 6px; flex: 1; justify-content: center;">
          <div style="background: #ffffff; border: 1px solid #cbd5e1; padding: 8px 10px; border-radius: 5px; font-size: 11.5px; text-align: center;">Sense Ambient Air</div>
          <div style="text-align: center; color: #94a3b8; font-size: 11px;">↓</div>
          <div style="background: #ffffff; border: 1px solid #cbd5e1; padding: 8px 10px; border-radius: 5px; font-size: 11.5px; text-align: center;">Display on Web / App</div>
          <div style="text-align: center; color: #94a3b8; font-size: 11px;">↓</div>
          <div style="background: #fee2e2; border: 1px solid #fca5a5; color: #991b1b; padding: 8px 10px; border-radius: 5px; font-size: 11.5px; text-align: center; font-weight: 700;">No Physical Mitigation</div>
        </div>
        <div style="margin-top: 10px; font-size: 11px; color: #be123c; font-weight: 600; border-top: 1px dashed #cbd5e1; padding-top: 8px;">
          ❌ Passive Observation Only: Informs workers they are being poisoned without acting.
        </div>
      </div>
      
      <!-- Column 2 -->
      <div style="flex: 1; background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 16px; display: flex; flex-direction: column;">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
          <span style="background: #e2e8f0; color: #334155; font-weight: 800; font-size: 11px; padding: 3px 8px; border-radius: 4px;">APPROACH 2</span>
          <h3 style="margin: 0; font-size: 15px; color: #1e3a8a;">Conventional Purification</h3>
        </div>
        <div style="font-size: 12.5px; color: #475569; margin-bottom: 12px;">
          Room or plant-scale mechanical HEPA air cleaners operating on feedback loops.
        </div>
        <div style="display: flex; flex-direction: column; gap: 6px; flex: 1; justify-content: center;">
          <div style="background: #ffffff; border: 1px solid #cbd5e1; padding: 8px 10px; border-radius: 5px; font-size: 11.5px; text-align: center;">Room-Scale Air Handling</div>
          <div style="text-align: center; color: #94a3b8; font-size: 11px;">↓</div>
          <div style="background: #ffffff; border: 1px solid #cbd5e1; padding: 8px 10px; border-radius: 5px; font-size: 11.5px; text-align: center;">Continuous Fan Run (High Power)</div>
          <div style="text-align: center; color: #94a3b8; font-size: 11px;">↓</div>
          <div style="background: #fee2e2; border: 1px solid #fca5a5; color: #991b1b; padding: 8px 10px; border-radius: 5px; font-size: 11.5px; text-align: center; font-weight: 700;">Reactive (Triggers AFTER Peak)</div>
        </div>
        <div style="margin-top: 10px; font-size: 11px; color: #be123c; font-weight: 600; border-top: 1px dashed #cbd5e1; padding-top: 8px;">
          ❌ Spatial & Cost Inefficiency: Thousands of watts needed; filters quickly clog in open plants.
        </div>
      </div>
      
      <!-- Column 3 -->
      <div style="flex: 1; background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 16px; display: flex; flex-direction: column;">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
          <span style="background: #e2e8f0; color: #334155; font-weight: 800; font-size: 11px; padding: 3px 8px; border-radius: 4px;">APPROACH 3</span>
          <h3 style="margin: 0; font-size: 15px; color: #1e3a8a;">Static AI Prediction</h3>
        </div>
        <div style="font-size: 12.5px; color: #475569; margin-bottom: 12px;">
          Offline deep learning or batch ML models trained on fixed historical records.
        </div>
        <div style="display: flex; flex-direction: column; gap: 6px; flex: 1; justify-content: center;">
          <div style="background: #ffffff; border: 1px solid #cbd5e1; padding: 8px 10px; border-radius: 5px; font-size: 11.5px; text-align: center;">Batch Training (Historical Data)</div>
          <div style="text-align: center; color: #94a3b8; font-size: 11px;">↓</div>
          <div style="background: #ffffff; border: 1px solid #cbd5e1; padding: 8px 10px; border-radius: 5px; font-size: 11.5px; text-align: center;">Fixed Weights Frozen at Deployment</div>
          <div style="text-align: center; color: #94a3b8; font-size: 11px;">↓</div>
          <div style="background: #fee2e2; border: 1px solid #fca5a5; color: #991b1b; padding: 8px 10px; border-radius: 5px; font-size: 11.5px; text-align: center; font-weight: 700;">No Site Adaptation / Drifts</div>
        </div>
        <div style="margin-top: 10px; font-size: 11px; color: #be123c; font-weight: 600; border-top: 1px dashed #cbd5e1; padding-top: 8px;">
          ❌ Concept Drift Vulnerability: Cannot adapt when moved between different factory clusters.
        </div>
      </div>
    </div>
    
    <!-- Bottom Integrated Synthesis Bar -->
    <div style="margin-top: 16px; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 12px 18px; display: flex; justify-content: space-between; align-items: center;">
      <div style="font-size: 13px; font-weight: 700; color: #1e3a8a;">The Resulting Engineering Dilemma:</div>
      <div style="display: flex; gap: 24px; font-size: 12px; color: #334155;">
        <span><strong>Spatial:</strong> Room-scale ≠ Worker Breathing Zone</span>
        <span><strong>Temporal:</strong> Reactive Action ≠ Hazard Prevention</span>
        <span><strong>Intelligence:</strong> Frozen Models ≠ Changing Hotspots</span>
        <span><strong>Economic:</strong> Prohibitive Capex ≠ SME Budgets</span>
      </div>
    </div>
  </div>
"""
add_slide("slide-3", "2. Limitations of Existing Systems", "Where Traditional Approaches Fall Short", "The fundamental fragmentation between sensing, prediction, and physical purification", "Literature Critique", slide_3_body)

print("Defining Slide 4...")
# SLIDE 4: Recent Research Landscape (2024–2026)
slide_4_body = """
  <div style="width: 100%; display: flex; flex-direction: column; justify-content: space-between; height: 100%;">
    <table class="academic-table">
      <thead>
        <tr>
          <th style="width: 18%;">Recent Study</th>
          <th style="width: 8%; text-align: center;">Year</th>
          <th style="width: 22%;">Main Approach</th>
          <th style="width: 10%; text-align: center;">Prediction?</th>
          <th style="width: 12%; text-align: center;">Purification?</th>
          <th style="width: 10%; text-align: center;">Adaptivity</th>
          <th style="width: 20%;">Identified Gap / Limitation</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Alam et al.</strong> (JARSET)</td>
          <td style="text-align: center;">2025</td>
          <td>Fixed IoT node for developing areas</td>
          <td style="text-align: center; color: #be123c;">No</td>
          <td style="text-align: center; color: #be123c;">No</td>
          <td style="text-align: center;">Static</td>
          <td>Observation only; no predictive or physical action</td>
        </tr>
        <tr>
          <td><strong>Ramadhani et al.</strong> (IEEE IAICT)</td>
          <td style="text-align: center;">2025</td>
          <td>Low-cost sensor IoT air monitoring</td>
          <td style="text-align: center; color: #be123c;">No</td>
          <td style="text-align: center; color: #be123c;">No</td>
          <td style="text-align: center;">Static</td>
          <td>Raw threshold alert; lacks predictive automation</td>
        </tr>
        <tr>
          <td><strong>Pavan et al.</strong> (IJSREM)</td>
          <td style="text-align: center;">2025</td>
          <td>IoT with buzzer & SMS alerts</td>
          <td style="text-align: center; color: #be123c;">No</td>
          <td style="text-align: center; color: #be123c;">No</td>
          <td style="text-align: center;">Static</td>
          <td>Reactive notification; zero physical remediation</td>
        </tr>
        <tr>
          <td><strong>Shabbir et al.</strong> (Env. Int.)</td>
          <td style="text-align: center;">2025</td>
          <td>Low-cost sensors in developing nations</td>
          <td style="text-align: center; color: #b45309;">Mixed</td>
          <td style="text-align: center; color: #be123c;">No</td>
          <td style="text-align: center;">Static</td>
          <td>Reviews monitoring barriers; no integrated mitigation</td>
        </tr>
        <tr>
          <td><strong>Ali et al.</strong> (Air Qual. Atmos.)</td>
          <td style="text-align: center;">2025</td>
          <td>Long-term PM2.5 hotspots in Bangladesh</td>
          <td style="text-align: center; color: #be123c;">No</td>
          <td style="text-align: center; color: #be123c;">No</td>
          <td style="text-align: center;">N/A</td>
          <td>Satellite/ground mapping; no real-time hotspot control</td>
        </tr>
        <tr>
          <td><strong>Basak et al.</strong> (J. Agrofor. Env.)</td>
          <td style="text-align: center;">2025</td>
          <td>Spatial PM2.5/PM10 Tejgaon Dhaka</td>
          <td style="text-align: center; color: #be123c;">No</td>
          <td style="text-align: center; color: #be123c;">No</td>
          <td style="text-align: center;">N/A</td>
          <td>Quantifies local exposure; proposes no engineering solution</td>
        </tr>
        <tr class="highlight-row">
          <td><strong>Aurnab & Khanam</strong> (WAS Pollution)</td>
          <td style="text-align: center;"><span class="badge-2026">2026</span></td>
          <td>Landfill gas dispersion & monitoring in Dhaka</td>
          <td style="text-align: center; color: #be123c;">No</td>
          <td style="text-align: center; color: #be123c;">No</td>
          <td style="text-align: center;">Static</td>
          <td>Emission dispersion modeling only; no worker mitigation</td>
        </tr>
        <tr class="highlight-row">
          <td><strong>Ghosh et al.</strong> (Heliyon)</td>
          <td style="text-align: center;"><span class="badge-2026">2026</span></td>
          <td>CO₂ spatiotemporal remote sensing over BD</td>
          <td style="text-align: center; color: #be123c;">No</td>
          <td style="text-align: center; color: #be123c;">No</td>
          <td style="text-align: center;">N/A</td>
          <td>Atmospheric observation; disconnected from localized physical action</td>
        </tr>
        <tr class="highlight-row">
          <td><strong>Jaegle</strong> (EngRxiv)</td>
          <td style="text-align: center;"><span class="badge-2026">2026</span></td>
          <td>Innovative particulate filtration technologies</td>
          <td style="text-align: center; color: #be123c;">No</td>
          <td style="text-align: center; color: #0f766e; font-weight: 700;">Yes (Mat.)</td>
          <td style="text-align: center;">Static</td>
          <td>Filter materials evaluation; lacks sensor-AI closed-loop</td>
        </tr>
        <tr class="highlight-row">
          <td><strong>Kabir et al.</strong> (Pollution)</td>
          <td style="text-align: center;"><span class="badge-2026">2026</span></td>
          <td>PM2.5 mortality & economic loss in 6 BD cities</td>
          <td style="text-align: center; color: #b45309;">Statistical</td>
          <td style="text-align: center; color: #be123c;">No</td>
          <td style="text-align: center;">N/A</td>
          <td>Macro public health loss ($23B); no hotspot engineering action</td>
        </tr>
        <tr class="champion-row">
          <td><strong>NirmalNode (This Thesis)</strong></td>
          <td style="text-align: center;"><span class="badge-2026">2026</span></td>
          <td>Hotspot Green IoT + Adaptive AI Purifier</td>
          <td style="text-align: center; color: #15803d; font-weight: 800;">Yes (1-2h)</td>
          <td style="text-align: center; color: #15803d; font-weight: 800;">Yes (Predictive)</td>
          <td style="text-align: center; color: #15803d; font-weight: 800;">Incremental</td>
          <td><strong>First closed-loop, adaptive, pre-emptive hotspot protection ($67)</strong></td>
        </tr>
      </tbody>
    </table>
    
    <div class="callout callout-teal" style="margin-top: 10px;">
      <strong>Authoritative Conclusion:</strong> Even the most recent 2024–2026 literature focuses overwhelmingly on <em>passive observation</em>, <em>satellite spatial mapping</em>, or <em>threshold alerts</em>. Closing the loop from predictive intelligence to localized physical mitigation with post-deployment online learning remains a totally unaddressed gap.
    </div>
  </div>
"""
add_slide("slide-4", "3. Literature Review", "Recent Research Landscape (2024–2026)", "Comparative analysis of recent studies verifying the persistence of the research gap", "State of the Art", slide_4_body)

print("Defining Slide 5...")
# SLIDE 5: Research Gap
slide_5_body = """
  <div style="width: 100%; display: flex; flex-direction: column; justify-content: space-between; height: 100%;">
    <!-- Visual Gap Architecture Diagram -->
    <div style="background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 18px 24px; display: flex; align-items: center; justify-content: space-between;">
      <div style="text-align: center; flex: 1;">
        <div style="background: #e0f2fe; color: #0369a1; font-weight: 800; font-size: 14px; padding: 10px; border-radius: 6px; border: 1px solid #bae6fd;">IoT Multi-Sensing</div>
        <div style="font-size: 11px; color: #64748b; margin-top: 4px;">PMS5003, MOS Gas Array</div>
      </div>
      
      <div style="color: #0f766e; font-size: 20px; font-weight: 800; padding: 0 12px;">➔</div>
      
      <div style="text-align: center; flex: 1;">
        <div style="background: #fef3c7; color: #b45309; font-weight: 800; font-size: 14px; padding: 10px; border-radius: 6px; border: 1px solid #fde68a;">AI Forecasting</div>
        <div style="font-size: 11px; color: #64748b; margin-top: 4px;">1–2 Hour Ahead Lookahead</div>
      </div>
      
      <div style="color: #be123c; font-size: 24px; font-weight: 900; padding: 0 16px;">⚡ THE CRITICAL GAP ⚡</div>
      
      <div style="text-align: center; flex: 1;">
        <div style="background: #dcfce7; color: #15803d; font-weight: 800; font-size: 14px; padding: 10px; border-radius: 6px; border: 1px solid #bbf7d0;">Local Physical Purification</div>
        <div style="font-size: 11px; color: #64748b; margin-top: 4px;">Cyclone + HEPA-H13 + Carbon</div>
      </div>
      
      <div style="color: #0f766e; font-size: 20px; font-weight: 800; padding: 0 12px;">➔</div>
      
      <div style="text-align: center; flex: 1;">
        <div style="background: #ede9fe; color: #6d28d9; font-weight: 800; font-size: 14px; padding: 10px; border-radius: 6px; border: 1px solid #ddd6fe;">Adaptive Online Learning</div>
        <div style="font-size: 11px; color: #64748b; margin-top: 4px;">River / Incremental SGD+PA</div>
      </div>
    </div>
    
    <!-- 6 Detailed Gap Statements from Thesis Table 2.2 -->
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 14px;">
      <div style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 3.5px solid #be123c; padding: 10px 14px; border-radius: 6px;">
        <div style="font-size: 12px; font-weight: 700; color: #be123c; margin-bottom: 3px;">1. Decoupled Architecture</div>
        <div style="font-size: 11.5px; color: #475569; line-height: 1.45;">Prior IoT and AI systems end at reporting or forecasting; they never couple the forecast to an automated physical mitigation response.</div>
      </div>
      
      <div style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 3.5px solid #be123c; padding: 10px 14px; border-radius: 6px;">
        <div style="font-size: 12px; font-weight: 700; color: #be123c; margin-bottom: 3px;">2. Room-Scale Misalignment</div>
        <div style="font-size: 11.5px; color: #475569; line-height: 1.45;">Purification literature tests room/vehicle scale cleaners (Dubey 2021, Lu 2023, Lee 2022). No studies design for compact worker-proximate hotspots.</div>
      </div>
      
      <div style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 3.5px solid #be123c; padding: 10px 14px; border-radius: 6px;">
        <div style="font-size: 12px; font-weight: 700; color: #be123c; margin-bottom: 3px;">3. Reactive Latency Lag</div>
        <div style="font-size: 11.5px; color: #475569; line-height: 1.45;">Conventional air cleaners react only after high pollutant levels are reached, meaning workers inhale the dangerous plume during the reaction delay.</div>
      </div>
      
      <div style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 3.5px solid #be123c; padding: 10px 14px; border-radius: 6px;">
        <div style="font-size: 12px; font-weight: 700; color: #be123c; margin-bottom: 3px;">4. Static AI Inflexibility</div>
        <div style="font-size: 11.5px; color: #475569; line-height: 1.45;">Existing air AI models are trained once offline. When relocated across distinct industrial zones, prediction accuracy severely degrades without retraining.</div>
      </div>
      
      <div style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 3.5px solid #be123c; padding: 10px 14px; border-radius: 6px;">
        <div style="font-size: 12px; font-weight: 700; color: #be123c; margin-bottom: 3px;">5. Evidence Without Engineering</div>
        <div style="font-size: 11.5px; color: #475569; line-height: 1.45;">Occupational studies prove acute worker health deterioration at hotspots, but propose no low-cost, retrofittable engineering countermeasure.</div>
      </div>
      
      <div style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 3.5px solid #be123c; padding: 10px 14px; border-radius: 6px;">
        <div style="font-size: 12px; font-weight: 700; color: #be123c; margin-bottom: 3px;">6. Cost & Adoption Barrier</div>
        <div style="font-size: 11.5px; color: #475569; line-height: 1.45;">High retail purifier prices lead to <1% adoption in Bangladesh. An ultra-low-cost, multi-sensor platform engineered for local SMEs is urgently needed.</div>
      </div>
    </div>
    
    <div style="margin-top: 10px; background: #f0fdfa; border: 1px solid #99f6e4; border-radius: 6px; padding: 10px 16px; text-align: center; font-size: 13px; color: #0f766e; font-weight: 700;">
      🎯 NirmalNode's Core Mandate: Bridge this gap by integrating sensing, 1–2h forecasting, pre-emptive physical action, and continuous online adaptation in a $67 unit.
    </div>
  </div>
"""
add_slide("slide-5", "4. Research Gap", "What Still Remains Unsolved?", "Synthesizing the exact technical voids identified in literature and Table 2.2", "Identified Research Gap", slide_5_body)

print("Defining Slide 6...")
# SLIDE 6: What Makes NirmalNode Different (Central Novelty)
slide_6_body = """
  <div style="width: 100%; display: flex; flex-direction: column; justify-content: space-between; height: 100%;">
    <!-- Central Visual Workflow Contrast -->
    <div style="display: flex; gap: 20px; align-items: stretch; flex: 1;">
      <!-- Traditional Column -->
      <div style="flex: 4; background: #f8fafc; border: 1.5px solid #cbd5e1; border-radius: 8px; padding: 16px; display: flex; flex-direction: column; justify-content: space-between;">
        <div style="text-align: center; border-bottom: 1.5px solid #e2e8f0; padding-bottom: 8px;">
          <span style="font-size: 11px; font-weight: 800; color: #64748b; text-transform: uppercase;">Existing Paradigm</span>
          <h3 style="color: #475569; margin-top: 2px; font-size: 16px;">Traditional Systems</h3>
        </div>
        
        <div style="display: flex; flex-direction: column; gap: 8px; padding: 12px 0;">
          <div style="background: #ffffff; border: 1px solid #cbd5e1; padding: 8px; border-radius: 6px; text-align: center; font-size: 12px; font-weight: 600;">1. Sense (City/Room Scale)</div>
          <div style="text-align: center; color: #94a3b8;">↓</div>
          <div style="background: #ffffff; border: 1px solid #cbd5e1; padding: 8px; border-radius: 6px; text-align: center; font-size: 12px; font-weight: 600;">2. Display / Predict (Static Model)</div>
          <div style="text-align: center; color: #94a3b8;">↓</div>
          <div style="background: #fee2e2; border: 1px solid #fca5a5; color: #991b1b; padding: 8px; border-radius: 6px; text-align: center; font-size: 12px; font-weight: 700;">3. Manual or Reactive Response</div>
        </div>
        
        <div style="background: #ffffff; border-radius: 6px; padding: 8px 12px; font-size: 11px; color: #64748b; line-height: 1.4;">
          <strong>Traits:</strong> Coarse spatial scale • Static offline AI • High latency • Disconnected hardware & software • $500–$2000 cost.
        </div>
      </div>
      
      <!-- Central VS Divider -->
      <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <div style="background: #1e3a8a; color: #ffffff; width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">VS</div>
      </div>
      
      <!-- NirmalNode Column -->
      <div style="flex: 6; background: #f0fdfa; border: 2px solid #0f766e; border-radius: 8px; padding: 16px; display: flex; flex-direction: column; justify-content: space-between;">
        <div style="text-align: center; border-bottom: 1.5px solid #ccfbf1; padding-bottom: 8px;">
          <span style="font-size: 11px; font-weight: 800; color: #0f766e; text-transform: uppercase;">Novel Contribution</span>
          <h3 style="color: #1e3a8a; margin-top: 2px; font-size: 17px;">NirmalNode Closed-Loop Architecture</h3>
        </div>
        
        <!-- Horizontal Step Chain -->
        <div style="display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px; align-items: center; margin: 12px 0;">
          <div style="background: #ffffff; border: 1px solid #0f766e; padding: 6px 2px; border-radius: 4px; text-align: center; font-size: 11px; font-weight: 700; color: #1e3a8a;">Sense<br><span style="font-size: 9px; color: #64748b; font-weight: 400;">Multi-Gas</span></div>
          <div style="text-align: center; color: #0f766e; font-weight: 800;">→</div>
          <div style="background: #ffffff; border: 1px solid #0f766e; padding: 6px 2px; border-radius: 4px; text-align: center; font-size: 11px; font-weight: 700; color: #1e3a8a;">Filter<br><span style="font-size: 9px; color: #64748b; font-weight: 400;">Edge EMA</span></div>
          <div style="text-align: center; color: #0f766e; font-weight: 800;">→</div>
          <div style="background: #ffffff; border: 1px solid #0f766e; padding: 6px 2px; border-radius: 4px; text-align: center; font-size: 11px; font-weight: 700; color: #1e3a8a;">Predict<br><span style="font-size: 9px; color: #64748b; font-weight: 400;">1–2h Look</span></div>
          <div style="text-align: center; color: #0f766e; font-weight: 800;">→</div>
          <div style="background: #ffffff; border: 1px solid #0f766e; padding: 6px 2px; border-radius: 4px; text-align: center; font-size: 11px; font-weight: 700; color: #1e3a8a;">Decide<br><span style="font-size: 9px; color: #64748b; font-weight: 400;">Threshold</span></div>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 4px; align-items: center; margin-bottom: 12px;">
          <div style="background: #dcfce7; border: 1px solid #16a34a; padding: 6px 2px; border-radius: 4px; text-align: center; font-size: 11px; font-weight: 700; color: #14532d;">Purify<br><span style="font-size: 9px; color: #15803d; font-weight: 400;">3-Stage</span></div>
          <div style="text-align: center; color: #0f766e; font-weight: 800;">→</div>
          <div style="background: #fef3c7; border: 1px solid #d97706; padding: 6px 2px; border-radius: 4px; text-align: center; font-size: 11px; font-weight: 700; color: #78350f;">Learn<br><span style="font-size: 9px; color: #b45309; font-weight: 400;">Prequential</span></div>
          <div style="text-align: center; color: #0f766e; font-weight: 800;">→</div>
          <div style="background: #ede9fe; border: 1px solid #7c3aed; padding: 6px 2px; border-radius: 4px; text-align: center; font-size: 11px; font-weight: 700; color: #4c1d95;">Adapt<br><span style="font-size: 9px; color: #6d28d9; font-weight: 400;">Site Shift</span></div>
        </div>
        
        <!-- 8 Explicit Novelties as short badges -->
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; font-size: 10.5px;">
          <div style="background: #ffffff; padding: 4px 6px; border-radius: 4px; border: 1px solid #ccfbf1;">🎯 <strong>Hotspot Scale</strong></div>
          <div style="background: #ffffff; padding: 4px 6px; border-radius: 4px; border: 1px solid #ccfbf1;">⏱️ <strong>Predictive Act.</strong></div>
          <div style="background: #ffffff; padding: 4px 6px; border-radius: 4px; border: 1px solid #ccfbf1;">🌱 <strong>Green IoT (ESP32)</strong></div>
          <div style="background: #ffffff; padding: 4px 6px; border-radius: 4px; border: 1px solid #ccfbf1;">⚡ <strong>Green AI (Light)</strong></div>
          <div style="background: #ffffff; padding: 4px 6px; border-radius: 4px; border: 1px solid #ccfbf1;">🔄 <strong>Online Learning</strong></div>
          <div style="background: #ffffff; padding: 4px 6px; border-radius: 4px; border: 1px solid #ccfbf1;">📍 <strong>Area-Adaptation</strong></div>
          <div style="background: #ffffff; padding: 4px 6px; border-radius: 4px; border: 1px solid #ccfbf1;">☁️ <strong>Edge + Cloud</strong></div>
          <div style="background: #ffffff; padding: 4px 6px; border-radius: 4px; border: 1px solid #ccfbf1;">💵 <strong>BDT 7,400 / $67</strong></div>
        </div>
      </div>
    </div>
  </div>
"""
add_slide("slide-6", "5. Core Novelty", "What Makes NirmalNode Different?", "The central answer to: What did you actually add beyond traditional systems?", "Core Innovation", slide_6_body)

print("Defining Slide 7...")
# SLIDE 7: Objectives
slide_7_body = """
  <div style="width: 100%; display: flex; flex-direction: column; justify-content: space-between; height: 100%;">
    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; flex: 1;">
      <!-- O1 -->
      <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-left: 4px solid #1e3a8a; border-radius: 6px; padding: 12px 16px; display: flex; gap: 14px; align-items: flex-start;">
        <div style="background: #1e3a8a; color: #ffffff; font-weight: 800; font-size: 14px; width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">O1</div>
        <div>
          <div style="font-size: 13.5px; font-weight: 700; color: #1e3a8a; margin-bottom: 3px;">Low-Cost Multi-Sensor IoT Node</div>
          <div style="font-size: 12px; color: #475569; line-height: 1.45;">Design and build an ESP32-based hardware node capable of continuously sampling PM1.0, PM2.5, PM10, CO, NO₂, VOC, NH₃, H₂S, and ambient temp/humidity/pressure at worker micro-zones.</div>
        </div>
      </div>
      
      <!-- O2 -->
      <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-left: 4px solid #0f766e; border-radius: 6px; padding: 12px 16px; display: flex; gap: 14px; align-items: flex-start;">
        <div style="background: #0f766e; color: #ffffff; font-weight: 800; font-size: 14px; width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">O2</div>
        <div>
          <div style="font-size: 13.5px; font-weight: 700; color: #0f766e; margin-bottom: 3px;">Cloud Telemetry & Ingestion Pipeline</div>
          <div style="font-size: 12px; color: #475569; line-height: 1.45;">Construct an edge-to-cloud telemetry pipeline using JSON payloads over Wi-Fi (HTTP REST / MQTT) with time-, day-, and location-tagged circular storage and live dashboarding.</div>
        </div>
      </div>
      
      <!-- O3 -->
      <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-left: 4px solid #d97706; border-radius: 6px; padding: 12px 16px; display: flex; gap: 14px; align-items: flex-start;">
        <div style="background: #d97706; color: #ffffff; font-weight: 800; font-size: 14px; width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">O3</div>
        <div>
          <div style="font-size: 13.5px; font-weight: 700; color: #d97706; margin-bottom: 3px;">1–2 Hour Ahead Pollution Forecasting</div>
          <div style="font-size: 12px; color: #475569; line-height: 1.45;">Develop an Adaptive AI model initially pre-trained on historical Bangladesh air-quality records, capable of forecasting hotspot-level PM2.5 concentrations 1–2 hours in advance.</div>
        </div>
      </div>
      
      <!-- O4 -->
      <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-left: 4px solid #7c3aed; border-radius: 6px; padding: 12px 16px; display: flex; gap: 14px; align-items: flex-start;">
        <div style="background: #7c3aed; color: #ffffff; font-weight: 800; font-size: 14px; width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">O4</div>
        <div>
          <div style="font-size: 13.5px; font-weight: 700; color: #7c3aed; margin-bottom: 3px;">Incremental (Online) Adaptive Learning</div>
          <div style="font-size: 12px; color: #475569; line-height: 1.45;">Implement stream-learning estimators (SGD Regressor, Passive-Aggressive, Hoeffding Trees) to update weights continuously without full retraining, adapting to area relocations.</div>
        </div>
      </div>
      
      <!-- O5 -->
      <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-left: 4px solid #16a34a; border-radius: 6px; padding: 12px 16px; display: flex; gap: 14px; align-items: flex-start;">
        <div style="background: #16a34a; color: #ffffff; font-weight: 800; font-size: 14px; width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">O5</div>
        <div>
          <div style="font-size: 13.5px; font-weight: 700; color: #16a34a; margin-bottom: 3px;">Localized 3-Stage Purification Subsystem</div>
          <div style="font-size: 12px; color: #475569; line-height: 1.45;">Design and prototype a worker-facing filtration train (cyclone separator, HEPA-H13 filter, activated-carbon pad, 12V fan) triggered automatically ahead of hazard threshold crossings.</div>
        </div>
      </div>
      
      <!-- O6 -->
      <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-left: 4px solid #be123c; border-radius: 6px; padding: 12px 16px; display: flex; gap: 14px; align-items: flex-start;">
        <div style="background: #be123c; color: #ffffff; font-weight: 800; font-size: 14px; width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">O6</div>
        <div>
          <div style="font-size: 13.5px; font-weight: 700; color: #be123c; margin-bottom: 3px;">Multi-Dimensional System Evaluation</div>
          <div style="font-size: 12px; color: #475569; line-height: 1.45;">Rigorously evaluate predictive accuracy (MAE, RMSE, R², F1), prequential convergence, physical filtration efficiency (PM1.0, PM2.5, PM10), power profile, and economic feasibility.</div>
        </div>
      </div>
    </div>
    
    <div class="callout callout-navy" style="margin-top: 12px;">
      <strong>Execution Plan:</strong> Objectives O1–O5 define the engineering realization (Chapter 3 Methodology), while O6 establishes the experimental validation (Chapter 4 Results).
    </div>
  </div>
"""
add_slide("slide-7", "6. Research Roadmap", "Research Objectives", "Clear, measurable engineering targets guiding system design and evaluation", "Research Goals", slide_7_body)

print("Defining Slide 8...")
# SLIDE 8: System Overview (Architecture & Workflow)
slide_8_body = """
  <div class="col-half" style="flex: 5.5;">
    <div class="img-frame" style="height: 100%;">
      <img src="figures_academic/five_layer_architecture_academic.png" alt="Figure 3.1 Five-Layer System Architecture" style="width: 100%; height: calc(100% - 24px); object-fit: contain;">
      <div class="img-caption">Figure 3.1: Five-layer system architecture of NirmalNode (Sensors → Edge MCU → Cloud DB → AI → Actuation)</div>
    </div>
  </div>
  
  <div class="col-half" style="flex: 4.5; justify-content: space-between;">
    <div class="img-frame" style="flex: 1; margin-bottom: 10px;">
      <img src="extracted_figs/system_workflow.png" alt="Figure 3.2 End-to-End Operational Workflow" style="width: 100%; height: calc(100% - 24px); object-fit: contain;">
      <div class="img-caption">Figure 3.2: Complete closed-loop operational workflow from multi-sensor polling to clean air delivery</div>
    </div>
    
    <div class="bullet-list" style="flex-shrink: 0; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 14px;">
      <div class="bullet-item">
        <div class="bullet-dot"></div>
        <div style="font-size: 12px;"><strong>Layer 1 (Sensing):</strong> 12-channel continuous acquisition at worker breathing zone.</div>
      </div>
      <div class="bullet-item">
        <div class="bullet-dot"></div>
        <div style="font-size: 12px;"><strong>Layer 2 (Edge MCU):</strong> ESP32 EMA signal smoothing (α=0.25) & packetization.</div>
      </div>
      <div class="bullet-item">
        <div class="bullet-dot"></div>
        <div style="font-size: 12px;"><strong>Layer 3 (Transport):</strong> High-throughput HTTP POST / MQTT telemetry ingest.</div>
      </div>
      <div class="bullet-item">
        <div class="bullet-dot"></div>
        <div style="font-size: 12px;"><strong>Layer 4 (Adaptive AI):</strong> 1–2 hr forecast + prequential online weight update.</div>
      </div>
      <div class="bullet-item">
        <div class="bullet-dot"></div>
        <div style="font-size: 12px;"><strong>Layer 5 (Actuation):</strong> Relay triggers Cyclone-HEPA-Carbon fan pre-emptively.</div>
      </div>
    </div>
  </div>
"""
add_slide("slide-8", "7. System Methodology", "NirmalNode: End-to-End System", "Layered technical architecture and the complete physical-to-intelligence loop", "System Architecture", slide_8_body)

print("Defining Slide 9...")
# SLIDE 9: Hardware Implementation
slide_9_body = """
  <div class="col-70">
    <div class="img-frame" style="height: 100%;">
      <img src="fig01_hardware_composite.png" alt="Figure 3.5 Prototype Hardware Architecture & Wiring" style="width: 100%; height: calc(100% - 24px); object-fit: contain;">
      <div class="img-caption">Figure 3.5: NirmalNode prototype hardware interfacing diagram (Source: Project Prototype / Thesis)</div>
    </div>
  </div>
  
  <div class="col-30" style="justify-content: space-between;">
    <div>
      <h3 style="font-size: 15px; margin-bottom: 8px;">Key Components (Table 3.1)</h3>
      <div style="display: flex; flex-direction: column; gap: 5px; font-size: 11px;">
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 5px 8px; border-radius: 4px;">
          <strong>ESP32 WROOM-32:</strong> Dual-core 240MHz, built-in Wi-Fi/BLE, ADC1, UART2.
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 5px 8px; border-radius: 4px;">
          <strong>PMS5003 Laser:</strong> PM1.0, PM2.5, PM10 (UART2 GPIO16/17).
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 5px 8px; border-radius: 4px;">
          <strong>MiCS-4514 Dual:</strong> CO (RED GPIO34) & NO₂ (OX GPIO35).
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 5px 8px; border-radius: 4px;">
          <strong>MQ135 & MQ136:</strong> VOC/NH₃/Smoke (GPIO32) & H₂S (GPIO33).
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 5px 8px; border-radius: 4px;">
          <strong>MP135:</strong> Relative VOC/Air Quality channel (GPIO36).
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 5px 8px; border-radius: 4px;">
          <strong>BME280:</strong> Ambient Temp, Relative Humidity, Pressure (I2C).
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 5px 8px; border-radius: 4px;">
          <strong>Relay + 12V DC Fan:</strong> Optocoupled relay (GPIO25), 0.5A exhaust fan.
        </div>
      </div>
    </div>
    
    <div class="callout callout-teal" style="font-size: 11px;">
      <strong>Green IoT Power Architecture:</strong> Powered by 3S Li-Po (11.1V, 55.5 Wh) + 3S BMS + Buck converter (11.1V → 5V 3A) for portable hotspot retrofitting.
    </div>
  </div>
"""
add_slide("slide-9", "8. Hardware Engineering", "Hardware Implementation", "Multi-sensor hardware integration centered on a single low-power ESP32 controller", "Hardware Subsystem", slide_9_body)

print("Defining Slide 10...")
# SLIDE 10: Hardware Architecture + Data Flow
slide_10_body = """
  <div class="col-60">
    <div class="img-frame" style="height: 100%;">
      <img src="extracted_figs/hardware_block_diagram.png" alt="Hardware Block Diagram" style="width: 100%; height: calc(100% - 24px); object-fit: contain;">
      <div class="img-caption">Figure 3.5b: Physical block diagram and bus-level interfacing between sensors, MCU, and actuators</div>
    </div>
  </div>
  
  <div class="col-40" style="justify-content: space-between;">
    <div>
      <h3 style="font-size: 15px; margin-bottom: 6px;">From Sensors to the AI Engine</h3>
      
      <div class="flow-step">
        <div class="step-num">1</div>
        <div class="step-content">
          <strong>Synchronous Acquisition (Δt = 2s):</strong> ESP32 polls digital UART2 packets from PMS5003 and 12-bit ADC channels for MOS gas sensors.
        </div>
      </div>
      
      <div class="flow-step">
        <div class="step-num">2</div>
        <div class="step-content">
          <strong>On-Device EMA Noise Filtering:</strong>
          <div style="background: #ffffff; border: 1px solid #cbd5e1; padding: 4px 8px; border-radius: 4px; font-family: monospace; font-size: 11px; margin: 3px 0;">
            x̂[k] = α · x_raw[k] + (1 - α) · x̂[k-1]
          </div>
          Smoothing parameter <strong>α = 0.25</strong> eliminates high-frequency sensor jitter while retaining fast plume tracking.
        </div>
      </div>
      
      <div class="flow-step">
        <div class="step-num">3</div>
        <div class="step-content">
          <strong>JSON Telemetry Formatting:</strong>
          Assembles calibrated channels into lightweight JSON:
          <div style="background: #ffffff; border: 1px solid #cbd5e1; padding: 3px 6px; border-radius: 4px; font-family: monospace; font-size: 9.5px; color: #0369a1; margin-top: 2px;">
            {"pm2_5":35, "mq135":1748, "mics_red":2219, ...}
          </div>
        </div>
      </div>
      
      <div class="flow-step">
        <div class="step-num">4</div>
        <div class="step-content">
          <strong>Low-Overhead Wireless Dispatch:</strong> Transmitted via Wi-Fi to Flask backend. Returns relay state <code>FAN_ON / FAN_OFF</code> in HTTP response.
        </div>
      </div>
    </div>
    
    <div class="callout callout-navy" style="font-size: 11px;">
      <strong>Edge Simplicity:</strong> Compute-heavy inference runs server-side, keeping the ESP32 code ultra-lightweight and power draw at just <strong>1.8 W</strong> in sensing mode.
    </div>
  </div>
"""
add_slide("slide-10", "9. Signal Processing", "From Sensors to the AI Engine", "Data acquisition flow, on-device noise filtering, and edge-to-cloud telemetry dispatch", "Sensor Data Pipeline", slide_10_body)

print("Defining Slide 11...")
# SLIDE 11: Software & Data Pipeline
slide_11_body = """
  <div class="col-60">
    <div class="img-frame" style="height: 100%;">
      <img src="software_block_diagram.png" alt="Figure 3.6 Software Block Diagram" style="width: 100%; height: calc(100% - 24px); object-fit: contain;">
      <div class="img-caption">Figure 3.6: Software block diagram spanning device-side firmware and server-side cloud services</div>
    </div>
  </div>
  
  <div class="col-40" style="justify-content: space-between;">
    <div>
      <h3 style="font-size: 15px; margin-bottom: 8px;">Software Architecture Breakdown</h3>
      
      <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px; margin-bottom: 8px;">
        <div style="font-size: 12px; font-weight: 700; color: #be123c; margin-bottom: 4px;">ESP32 Firmware (AirGuard_WiFi.ino)</div>
        <div style="font-size: 11px; color: #475569; line-height: 1.45;">
          • Power-on 48-hour burn-in baseline calibration (<code>calibrateSensors()</code>)<br>
          • 2-second non-blocking timer interrupt loop<br>
          • In-situ EMA noise filtering and temperature compensation<br>
          • Direct GPIO25 relay driver switching 12V DC fan
        </div>
      </div>
      
      <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px; margin-bottom: 8px;">
        <div style="font-size: 12px; font-weight: 700; color: #0f766e; margin-bottom: 4px;">Python Flask Backend (server.py)</div>
        <div style="font-size: 11px; color: #475569; line-height: 1.45;">
          • High-throughput REST API endpoint <code>/api/ingest</code><br>
          • Synchronous call to <code>AdaptiveAIEngine.predict_and_learn()</code><br>
          • In-memory circular telemetry buffer (500 records)<br>
          • Returns purifier relay command synchronously in HTTP body
        </div>
      </div>
      
      <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px;">
        <div style="font-size: 12px; font-weight: 700; color: #1e3a8a; margin-bottom: 4px;">Client Web Dashboard (app.js / index.html)</div>
        <div style="font-size: 11px; color: #475569; line-height: 1.45;">
          • 2-second polling of <code>/api/latest</code> telemetry<br>
          • Real-time AQI gauge, multi-gas bar array, Chart.js time-series<br>
          • Auto-AI / Manual purifier control override switches
        </div>
      </div>
    </div>
    
    <div class="callout callout-teal" style="font-size: 11px;">
      <strong>Zero Latency:</strong> Decision calculation executes in <strong><15 ms</strong>, returning the fan trigger to the ESP32 in the very same HTTP round-trip.
    </div>
  </div>
"""
add_slide("slide-11", "10. Software Engineering", "Software and Data Processing Pipeline", "Firmware routines, server-side ingestion, and the closed-loop actuator feedback cycle", "Software Architecture", slide_11_body)

print("Defining Slide 12...")
# SLIDE 12: Adaptive AI Engine
slide_12_body = """
  <div class="col-half" style="flex: 5.5;">
    <div class="img-frame" style="height: 100%;">
      <img src="extracted_figs/ai_model_arena_pipeline.png" alt="Figure 3.7 AI Model Arena Pipeline" style="width: 100%; height: calc(100% - 24px); object-fit: contain;">
      <div class="img-caption">Figure 3.7: Adaptive AI pipeline: Initial batch pre-training to streaming incremental prequential learning</div>
    </div>
  </div>
  
  <div class="col-half" style="flex: 4.5; justify-content: space-between;">
    <div>
      <div class="callout callout-teal" style="margin-top: 0; margin-bottom: 10px;">
        <strong style="font-size: 13px;">Core Novelty: NO FULL RETRAINING REQUIRED</strong><br>
        Models update parameters sample-by-sample via the <strong>prequential (test-then-train)</strong> protocol using the open-source River and scikit-learn libraries.
      </div>
      
      <h3 style="font-size: 14px; margin-bottom: 6px;">9 Candidate Models Evaluated in Arena</h3>
      <div style="display: flex; flex-direction: column; gap: 4px; font-size: 11.5px;">
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 4px 8px; border-radius: 4px;">
          <strong>M1–M3:</strong> SGD Ridge (L2), Lasso (L1), ElasticNet (L1+L2).
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 4px 8px; border-radius: 4px;">
          <strong>M4:</strong> SGD Huber Regressor (Robust against severe smoke outliers).
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 4px 8px; border-radius: 4px;">
          <strong>M5:</strong> SGD Support Vector Regressor (SVR).
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 4px 8px; border-radius: 4px;">
          <strong>M6–M7:</strong> Passive-Aggressive Regressors (C=1.0 aggressive, C=0.1 cautious).
        </div>
        <div style="background: #e0f2fe; border: 1.5px solid #0284c7; padding: 5px 8px; border-radius: 4px; font-weight: 700; color: #0369a1;">
          ⭐ M8 (Champion): SGD + Passive-Aggressive Blend (Lowest MAE).
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 4px 8px; border-radius: 4px;">
          <strong>M9:</strong> Exponential Moving Average Baseline (Static reference).
        </div>
      </div>
    </div>
    
    <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 6px; padding: 8px 12px; font-size: 11px; color: #1e3a8a;">
      <strong>Area-Specific Adaptation:</strong> When a node is relocated (e.g., from Gazipur garment cluster to Narayanganj textile dyeing), incoming stream gradients automatically re-tune weights to the new site signature without human supervision.
    </div>
  </div>
"""
add_slide("slide-12", "11. Adaptive AI Engine", "Adaptive AI: Prediction That Keeps Learning", "Streaming incremental learning algorithms that eliminate batch retraining overhead", "Machine Learning Pipeline", slide_12_body)

print("Defining Slide 13...")
# SLIDE 13: Predictive Decision Engine
slide_13_body = """
  <div class="col-half" style="flex: 4.8;">
    <div class="img-frame" style="height: 100%;">
      <img src="extracted_figs/purifier_decision_flowchart.png" alt="Figure 3.9 Purifier Decision Flowchart" style="width: 100%; height: calc(100% - 24px); object-fit: contain;">
      <div class="img-caption">Figure 3.9: Threshold-based closed-loop purifier decision flowchart (Algorithm 2)</div>
    </div>
  </div>
  
  <div class="col-half" style="flex: 5.2; justify-content: space-between;">
    <div>
      <h3 style="font-size: 15px; margin-bottom: 8px;">From Prediction to Physical Action</h3>
      
      <div class="callout callout-teal" style="margin-top: 0; margin-bottom: 12px;">
        <strong>Decision Engine Logic (Equation 3.12):</strong>
        <div style="font-family: monospace; font-size: 12px; margin-top: 4px; font-weight: 700;">
          d_t = FAN_ON &nbsp;if ŷ_(t+h) ≥ τ_hazard (35.5 μg/m³)<br>
          d_t = FAN_OFF if ŷ_(t+h) < τ_hazard
        </div>
      </div>
      
      <div style="display: flex; flex-direction: column; gap: 8px; margin-bottom: 12px;">
        <div style="background: #fee2e2; border-left: 3.5px solid #be123c; padding: 8px 12px; border-radius: 0 6px 6px 0;">
          <div style="font-size: 11.5px; font-weight: 700; color: #991b1b;">Reactive Purifier (Traditional Failure):</div>
          <div style="font-size: 11px; color: #7f1d1d;">Pollution rises → Crosses threshold → Sensor detects → Fan starts → <em>Worker has already inhaled the peak plume.</em></div>
        </div>
        
        <div style="background: #dcfce7; border-left: 3.5px solid #15803d; padding: 8px 12px; border-radius: 0 6px 6px 0;">
          <div style="font-size: 11.5px; font-weight: 700; color: #14532d;">Predictive Purifier (NirmalNode Advantage):</div>
          <div style="font-size: 11px; color: #14532d;">AI forecasts spike 1–2h ahead → Fan activates pre-emptively → Chamber airflow establishes → <em>Breathing zone cleared BEFORE hazard peaks!</em></div>
        </div>
      </div>
      
      <div class="bullet-list">
        <div class="bullet-item">
          <div class="bullet-dot"></div>
          <div style="font-size: 12px;"><strong>Laboratory Verification:</strong> Pre-emptive trigger fired <strong>4–6 seconds before</strong> incoming incense-smoke concentration crossed 35.5 μg/m³ at the inlet probe.</div>
        </div>
        <div class="bullet-item">
          <div class="bullet-dot"></div>
          <div style="font-size: 12px;"><strong>Hysteresis Safety Buffer:</strong> Built-in run-down timer prevents rapid relay chatter during marginal threshold fluctuations.</div>
        </div>
      </div>
    </div>
    
    <div class="callout callout-navy" style="font-size: 11px;">
      <strong>Closed Feedback:</strong> After actuation, clean air delivery is registered by downstream sensors, closing the feedback loop and providing immediate reward/loss signal to the AI model.
    </div>
  </div>
"""
add_slide("slide-13", "12. Decision Engine", "From Prediction to Physical Action", "Threshold-based predictive activation closing the loop between AI forecasts and hardware", "Actuation Logic", slide_13_body)

print("Defining Slide 14...")
# SLIDE 14: Purification Subsystem
slide_14_body = """
  <div style="width: 100%; display: flex; flex-direction: column; justify-content: space-between; height: 100%;">
    <!-- Top Purification Pipeline Diagram -->
    <div class="img-frame" style="flex: 4.8; width: 100%;">
      <img src="extracted_figs/purification_pipeline.png" alt="Figure 3.3 Three-Stage Cyclone-HEPA-Carbon Purification Train" style="width: 100%; height: calc(100% - 22px); object-fit: contain;">
      <div class="img-caption">Figure 3.3: Local air purification train (Cyclone separator → HEPA-H13 filter → Activated carbon bed)</div>
    </div>
    
    <!-- 3 Stage Breakdown Columns -->
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; flex: 5.2; margin-top: 10px;">
      <!-- Stage 1 -->
      <div style="background: #f8fafc; border: 1.5px solid #e2e8f0; border-top: 3.5px solid #d97706; border-radius: 6px; padding: 12px; display: flex; flex-direction: column; justify-content: space-between;">
        <div>
          <div style="font-size: 11px; font-weight: 700; color: #d97706; text-transform: uppercase;">Stage 1: Pre-Filter</div>
          <h3 style="font-size: 14px; margin: 2px 0 6px 0; color: #1e3a8a;">Cyclone Separator</h3>
          <div style="font-size: 11.5px; color: #475569; line-height: 1.45;">
            • Tangential swirl induces centrifugal force: <code>F_c = m·v_t² / r</code><br>
            • Extracts heavy coarse particles (<strong>>10 μm</strong>: metal shavings, wood dust, grit)<br>
            • Critical Role: <strong>Extends expensive HEPA filter lifespan by 3×–5×</strong> by preventing surface dust caking.
          </div>
        </div>
        <div style="background: #fef3c7; color: #92400e; font-size: 11px; font-weight: 700; padding: 4px 8px; border-radius: 4px; text-align: center;">
          Coarse Particulate Pre-Cleaning
        </div>
      </div>
      
      <!-- Stage 2 -->
      <div style="background: #f8fafc; border: 1.5px solid #e2e8f0; border-top: 3.5px solid #2563eb; border-radius: 6px; padding: 12px; display: flex; flex-direction: column; justify-content: space-between;">
        <div>
          <div style="font-size: 11px; font-weight: 700; color: #2563eb; text-transform: uppercase;">Stage 2: Fine Particulate</div>
          <h3 style="font-size: 14px; margin: 2px 0 6px 0; color: #1e3a8a;">HEPA-H13 Filter</h3>
          <div style="font-size: 11.5px; color: #475569; line-height: 1.45;">
            • High-efficiency dense micro-glass fiber mat<br>
            • Certified <strong>≥99.97%</strong> retention of 0.3 μm particles<br>
            • Measured Prototype Efficiency (Table 4.8):<br>
            &nbsp;&nbsp;→ PM1.0: <strong>95.7%</strong> (42 → 1.8 μg/m³)<br>
            &nbsp;&nbsp;→ PM2.5: <strong>95.7%</strong> (67 → 2.9 μg/m³)<br>
            &nbsp;&nbsp;→ PM10: <strong>98.6%</strong> (Combined with cyclone)
          </div>
        </div>
        <div style="background: #dbeafe; color: #1e40af; font-size: 11px; font-weight: 700; padding: 4px 8px; border-radius: 4px; text-align: center;">
          95.7% PM2.5 Removal Efficiency
        </div>
      </div>
      
      <!-- Stage 3 -->
      <div style="background: #f8fafc; border: 1.5px solid #e2e8f0; border-top: 3.5px solid #7c3aed; border-radius: 6px; padding: 12px; display: flex; flex-direction: column; justify-content: space-between;">
        <div>
          <div style="font-size: 11px; font-weight: 700; color: #7c3aed; text-transform: uppercase;">Stage 3: Gaseous & Odour</div>
          <h3 style="font-size: 14px; margin: 2px 0 6px 0; color: #1e3a8a;">Activated Carbon Bed</h3>
          <div style="font-size: 11.5px; color: #475569; line-height: 1.45;">
            • Microporous surface area (>1000 m²/g)<br>
            • Langmuir physical adsorption: removes VOCs, CO, NO₂, NH₃, and toxic H₂S<br>
            • Measured: <strong>~60–70%</strong> qualitative VOC reduction; H₂S dropped below detection limit.
          </div>
        </div>
        <div style="background: #ede9fe; color: #5b21b6; font-size: 11px; font-weight: 700; padding: 4px 8px; border-radius: 4px; text-align: center;">
          Scientific Fact: HEPA Cannot Filter Gases
        </div>
      </div>
    </div>
  </div>
"""
add_slide("slide-14", "13. Purification Subsystem", "Localized 3-Stage Air Purification", "Sequential physical separation: Cyclone pre-filter → HEPA-H13 → Activated Carbon bed", "Filtration Train", slide_14_body)

print("Defining Slide 15...")
# SLIDE 15: Experimental Setup & Dashboard
slide_15_body = """
  <div class="col-half" style="flex: 5;">
    <div class="img-frame" style="height: 100%;">
      <img src="extracted_figs/dashboard_screenshot.jpg" alt="Figure 4.1 Real-Time Web Dashboard" style="width: 100%; height: calc(100% - 24px); object-fit: contain;">
      <div class="img-caption">Figure 4.1: NirmalNode real-time web dashboard (AQI gauge, 1h/2h AI forecasts, sensor cards, auto-AI fan)</div>
    </div>
  </div>
  
  <div class="col-half" style="flex: 5; justify-content: space-between;">
    <div class="img-frame" style="height: 52%; margin-bottom: 10px;">
      <img src="extracted_figs/xai_dashboard_screenshot.jpg" alt="Figure 4.7 XAI Dashboard Screenshot" style="width: 100%; height: calc(100% - 22px); object-fit: contain;">
      <div class="img-caption">Figure 4.7: Explainable AI dashboard showing live SHAP feature contributions and active AI purifier status</div>
    </div>
    
    <div>
      <h3 style="font-size: 14px; margin-bottom: 6px;">Evaluation Methodology & Test Environments</h3>
      <div class="bullet-list" style="font-size: 12px; gap: 5px;">
        <div class="bullet-item">
          <div class="bullet-dot"></div>
          <div><strong>Controlled Bench Lab:</strong> Physical prototype tested with localized incense-smoke spike injection (~15 cm from inlet) to validate sensor response and closed-loop relay trigger.</div>
        </div>
        <div class="bullet-item">
          <div class="bullet-dot"></div>
          <div><strong>Prequential Stream Benchmark:</strong> 500-sample industrial stream (sinusoidal baseline mean 28.3 μg/m³, periodic combustion spikes up to 77 μg/m³, Δt=2s) testing continuous online learning.</div>
        </div>
        <div class="bullet-item">
          <div class="bullet-dot"></div>
          <div><strong>Scientific Honesty Note:</strong> Quantitative AI prequential accuracy is evaluated on the calibrated simulation stream; hardware bench test validates physical trigger and airflow.</div>
        </div>
      </div>
    </div>
  </div>
"""
add_slide("slide-15", "14. Experimental Design", "Prototype and Experimental Evaluation", "Test environments, evaluation protocol, and real-time operational dashboard interfaces", "Experimental Setup", slide_15_body)

print("Defining Slide 16...")
# SLIDE 16: AI Results
slide_16_body = """
  <div style="width: 100%; display: flex; flex-direction: column; justify-content: space-between; height: 100%;">
    <!-- Top Visuals: Model Comparison Bar Chart + Confusion Matrix -->
    <div style="display: flex; gap: 16px; flex: 1; min-height: 0;">
      <div class="img-frame" style="flex: 5.8;">
        <img src="extracted_figs/model_arena_comparison.png" alt="Figure 4.2 Model Comparison Chart" style="width: 100%; height: calc(100% - 22px); object-fit: contain;">
        <div class="img-caption">Figure 4.2: Prequential forecasting error across 9 incremental models (Champion M8 lowest MAE = 10.62 μg/m³)</div>
      </div>
      
      <div class="img-frame" style="flex: 4.2;">
        <img src="extracted_figs/confusion_matrix.png" alt="Figure 4.3 Confusion Matrix" style="width: 100%; height: calc(100% - 22px); object-fit: contain;">
        <div class="img-caption">Figure 4.3: Purifier trigger confusion matrix (N=500, Hazard threshold = 35.5 μg/m³)</div>
      </div>
    </div>
    
    <!-- Bottom KPI Stat Row -->
    <div class="kpi-row" style="margin-top: 10px;">
      <div class="kpi-card">
        <div class="kpi-value">10.62</div>
        <div class="kpi-label">MAE (μg/m³)</div>
        <div class="kpi-sub">Baseline was 15.8</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">17.43</div>
        <div class="kpi-label">RMSE (μg/m³)</div>
        <div class="kpi-sub">Baseline was 24.3</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value teal">0.7334</div>
        <div class="kpi-label">R² Score</div>
        <div class="kpi-sub">Strong fit on stream</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value green">0.940</div>
        <div class="kpi-label">Hazard F1-Score</div>
        <div class="kpi-sub">Prec: 91.6% | Rec: 96.5%</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value green">97.2%</div>
        <div class="kpi-label">Overall Accuracy</div>
        <div class="kpi-sub">AUC-ROC: 0.985</div>
      </div>
      <div class="kpi-card" style="border: 1.5px solid #16a34a; background: #f0fdf4;">
        <div class="kpi-value green">0.8%</div>
        <div class="kpi-label">Missed Hazard Rate</div>
        <div class="kpi-sub">Only 4 FN in 500 samples!</div>
      </div>
    </div>
  </div>
"""
add_slide("slide-16", "15. Quantitative AI Results", "Adaptive AI Performance", "Prequential evaluation metrics, model comparison arena, and hazard-detection verification", "Experimental Findings", slide_16_body)

print("Defining Slide 17...")
# SLIDE 17: Adaptivity + XAI Results
slide_17_body = """
  <div class="col-half" style="flex: 5.2;">
    <div class="img-frame" style="height: 100%;">
      <img src="extracted_figs/prequential_error_plot.jpg" alt="Figure 4.6 Prequential Error Convergence" style="width: 100%; height: calc(100% - 24px); object-fit: contain;">
      <div class="img-caption">Figure 4.6: Prequential error convergence curve (Cold Start → Adaptation → Convergence)</div>
    </div>
  </div>
  
  <div class="col-half" style="flex: 4.8; justify-content: space-between;">
    <div class="img-frame" style="height: 54%; margin-bottom: 10px;">
      <img src="extracted_figs/xai_feature_importance.png" alt="Figure 4.8 Global Feature Importance" style="width: 100%; height: calc(100% - 22px); object-fit: contain;">
      <div class="img-caption">Figure 4.8: Global feature importance via Linear Feature Contribution (LFC / Exact SHAP)</div>
    </div>
    
    <div>
      <div class="callout callout-teal" style="margin-top: 0; margin-bottom: 8px;">
        <strong>Validation of the Adaptivity Claim:</strong>
        <div style="font-size: 11.5px; margin-top: 3px;">
          • <strong>Phase 1 (Cold Start, N=1–50):</strong> High initial MAE = <strong>33.4 μg/m³</strong>.<br>
          • <strong>Phase 2 (Adaptation, N=50–200):</strong> Rapid error collapse as weights adjust.<br>
          • <strong>Phase 3 (Convergence, N=200–500):</strong> Stabilizes at <strong>10.62 μg/m³</strong>.<br>
          ➔ <strong>68% error reduction</strong> achieved purely from live data without batch retraining!
        </div>
      </div>
      
      <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px; font-size: 11px; color: #334155;">
        <strong>XAI Transparency:</strong> Model relies primarily on physical temporal signals: PM2.5 EMA trend (0.224), current PM2.5 (0.186), PM10 (0.142), and fine particle count (0.118)—ruling out spurious correlations.
      </div>
    </div>
  </div>
"""
add_slide("slide-17", "16. Online Adaptation & XAI", "Adaptation and Explainability", "Empirical proof of incremental convergence and transparent SHAP feature contributions", "Adaptivity Evidence", slide_17_body)

print("Defining Slide 18...")
# SLIDE 18: Purification + Power + Cost Results
slide_18_body = """
  <div style="width: 100%; display: flex; gap: 16px; height: 100%;">
    <!-- Left Column: Purification & Power -->
    <div style="flex: 4.2; display: flex; flex-direction: column; justify-content: space-between;">
      <!-- Purification Table -->
      <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px;">
        <h3 style="font-size: 13.5px; margin-bottom: 6px; color: #1e3a8a;">Purification Efficiency (Table 4.8)</h3>
        <table class="academic-table" style="font-size: 11px;">
          <thead>
            <tr>
              <th>Pollutant</th>
              <th>Inlet</th>
              <th>Outlet</th>
              <th>Efficiency</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>PM1.0</strong></td>
              <td>42 μg/m³</td>
              <td>1.8 μg/m³</td>
              <td style="color: #15803d; font-weight: 800;">95.7%</td>
            </tr>
            <tr>
              <td><strong>PM2.5</strong></td>
              <td>67 μg/m³</td>
              <td>2.9 μg/m³</td>
              <td style="color: #15803d; font-weight: 800;">95.7%</td>
            </tr>
            <tr>
              <td><strong>PM10</strong></td>
              <td>98 μg/m³</td>
              <td>1.4 μg/m³</td>
              <td style="color: #15803d; font-weight: 800;">98.6%</td>
            </tr>
            <tr>
              <td><strong>VOC / Odour</strong></td>
              <td>Elevated</td>
              <td>Reduced</td>
              <td style="color: #0f766e; font-weight: 700;">~60–70%</td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Power Profile -->
      <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px;">
        <h3 style="font-size: 13.5px; margin-bottom: 6px; color: #1e3a8a;">Power Consumption Profile (Table 4.9)</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; font-size: 11px;">
          <div style="background: #ffffff; border: 1px solid #cbd5e1; padding: 6px 8px; border-radius: 4px;">
            <div style="color: #64748b;">Standby (Sensing):</div>
            <div style="font-size: 14px; font-weight: 800; color: #1e3a8a;">≈ 1.8 W</div>
          </div>
          <div style="background: #ffffff; border: 1px solid #cbd5e1; padding: 6px 8px; border-radius: 4px;">
            <div style="color: #64748b;">Wi-Fi Transmit:</div>
            <div style="font-size: 14px; font-weight: 800; color: #0f766e;">≈ 2.6 W</div>
          </div>
          <div style="background: #ffffff; border: 1px solid #cbd5e1; padding: 6px 8px; border-radius: 4px;">
            <div style="color: #64748b;">Purifier Fan Full ON:</div>
            <div style="font-size: 14px; font-weight: 800; color: #b45309;">≈ 6.0 W</div>
          </div>
          <div style="background: #fef2f2; border: 1px solid #fecaca; padding: 6px 8px; border-radius: 4px;">
            <div style="color: #991b1b; font-weight: 700;">Worst Case Total:</div>
            <div style="font-size: 14px; font-weight: 900; color: #be123c;">≈ 8.6 W</div>
          </div>
        </div>
        <div style="font-size: 10.5px; color: #475569; margin-top: 6px; line-height: 1.35;">
          🔋 <strong>55.5 Wh Li-Po Battery Life:</strong> ~30 hrs in standby; <strong>~17 hrs effective shift runtime</strong> at 25% duty cycle.
        </div>
      </div>
    </div>
    
    <!-- Right Column: BOM Cost Table -->
    <div style="flex: 5.8; background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 6px; padding: 12px; display: flex; flex-direction: column; justify-content: space-between;">
      <div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
          <h3 style="font-size: 14px; margin: 0; color: #1e3a8a;">Prototype Bill of Materials (Table 4.10)</h3>
          <span style="font-size: 10.5px; color: #64748b; font-style: italic;">Retail Pricing in Bangladesh (BDT 110/USD)</span>
        </div>
        
        <table class="academic-table" style="font-size: 10.5px;">
          <thead>
            <tr>
              <th>Component</th>
              <th style="text-align: center;">Qty</th>
              <th style="text-align: right;">Est. Cost (BDT)</th>
              <th style="text-align: right;">Est. Cost (USD)</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>ESP32 Dev Module (WROOM-32)</td><td style="text-align: center;">1</td><td style="text-align: right;">350</td><td style="text-align: right;">$3.18</td></tr>
            <tr><td>PMS5003 Laser Particulate Sensor</td><td style="text-align: center;">1</td><td style="text-align: right;">2,200</td><td style="text-align: right;">$20.00</td></tr>
            <tr><td>MiCS-4514 Dual Gas Sensor (CO/NO₂)</td><td style="text-align: center;">1</td><td style="text-align: right;">1,650</td><td style="text-align: right;">$15.00</td></tr>
            <tr><td>MQ135 Gas Sensor Module (VOC/NH₃)</td><td style="text-align: center;">1</td><td style="text-align: right;">180</td><td style="text-align: right;">$1.64</td></tr>
            <tr><td>MQ136 Gas Sensor Module (H₂S)</td><td style="text-align: center;">1</td><td style="text-align: right;">220</td><td style="text-align: right;">$2.00</td></tr>
            <tr><td>MP135 Sensor Module (Air Quality)</td><td style="text-align: center;">1</td><td style="text-align: right;">180</td><td style="text-align: right;">$1.64</td></tr>
            <tr><td>BME280 Environmental Sensor (T/H/P)</td><td style="text-align: center;">1</td><td style="text-align: right;">280</td><td style="text-align: right;">$2.55</td></tr>
            <tr><td>5V Relay Module (Fan Control)</td><td style="text-align: center;">1</td><td style="text-align: right;">90</td><td style="text-align: right;">$0.82</td></tr>
            <tr><td>12V DC Brushless Fan</td><td style="text-align: center;">1</td><td style="text-align: right;">400</td><td style="text-align: right;">$3.64</td></tr>
            <tr><td>Cyclone Separator (Fabricated)</td><td style="text-align: center;">1</td><td style="text-align: right;">350</td><td style="text-align: right;">$3.18</td></tr>
            <tr><td>HEPA-H13 Filter Element</td><td style="text-align: center;">1</td><td style="text-align: right;">650</td><td style="text-align: right;">$5.91</td></tr>
            <tr><td>Activated Carbon Filter Pad</td><td style="text-align: center;">1</td><td style="text-align: right;">250</td><td style="text-align: right;">$2.27</td></tr>
            <tr><td>Enclosure, Wiring, PCB, Connectors</td><td style="text-align: center;">1 set</td><td style="text-align: right;">600</td><td style="text-align: right;">$5.45</td></tr>
            <tr class="total-row">
              <td><strong>TOTAL PROTOTYPE COST</strong></td>
              <td style="text-align: center;"><strong>1 unit</strong></td>
              <td style="text-align: right; color: #1e3a8a;"><strong>7,400 BDT</strong></td>
              <td style="text-align: right; color: #1e3a8a;"><strong>$67.27 USD</strong></td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <div style="background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 4px; padding: 6px 10px; font-size: 11px; color: #065f46; margin-top: 6px;">
        💡 <strong>Commercial Comparison:</strong> At $67.27, NirmalNode is <strong>~10× cheaper</strong> than commercial room purifiers available in Bangladesh—which lack multi-gas sensing and predictive activation entirely.
      </div>
    </div>
  </div>
"""
add_slide("slide-18", "17. Practical Feasibility", "Practical Feasibility: Purification, Energy and Cost", "Authoritative verification of filtration efficiency, power budget, and BOM economics", "Engineering Feasibility", slide_18_body)

print("Defining Slide 19...")
# SLIDE 19: Novelty + Contributions
slide_19_body = """
  <div style="width: 100%; display: flex; flex-direction: column; justify-content: space-between; height: 100%;">
    <!-- Central Hub Architecture (Not a box grid!) -->
    <div style="flex: 1; position: relative; background: radial-gradient(circle at center, #f0fdfa 0%, #f8fafc 70%); border: 1.5px solid #ccfbf1; border-radius: 12px; padding: 20px; display: flex; align-items: center; justify-content: center;">
      
      <!-- Central Hub -->
      <div style="background: #1e3a8a; color: #ffffff; border: 4px solid #38bdf8; border-radius: 50%; width: 140px; height: 140px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.4); z-index: 10;">
        <div style="font-size: 17px; font-weight: 900; letter-spacing: -0.5px;">NIRMALNODE</div>
        <div style="font-size: 9.5px; font-weight: 600; color: #bae6fd; text-transform: uppercase; margin-top: 2px;">Integrated System</div>
      </div>
      
      <!-- 8 Satellite Contribution Badges Arranged Radially -->
      <div style="position: absolute; top: 16px; left: 32px; background: #ffffff; border: 1.5px solid #0f766e; padding: 8px 14px; border-radius: 20px; font-size: 12px; font-weight: 700; color: #0f766e; box-shadow: 0 2px 5px rgba(0,0,0,0.04);">
        🎯 Localized Hotspot Purification
      </div>
      
      <div style="position: absolute; top: 16px; right: 32px; background: #ffffff; border: 1.5px solid #0f766e; padding: 8px 14px; border-radius: 20px; font-size: 12px; font-weight: 700; color: #0f766e; box-shadow: 0 2px 5px rgba(0,0,0,0.04);">
        ⏱️ Predictive Activation (1–2h)
      </div>
      
      <div style="position: absolute; top: 50%; left: 16px; transform: translateY(-50%); background: #ffffff; border: 1.5px solid #0f766e; padding: 8px 14px; border-radius: 20px; font-size: 12px; font-weight: 700; color: #0f766e; box-shadow: 0 2px 5px rgba(0,0,0,0.04);">
        🔄 Incremental Streaming AI
      </div>
      
      <div style="position: absolute; top: 50%; right: 16px; transform: translateY(-50%); background: #ffffff; border: 1.5px solid #0f766e; padding: 8px 14px; border-radius: 20px; font-size: 12px; font-weight: 700; color: #0f766e; box-shadow: 0 2px 5px rgba(0,0,0,0.04);">
        🌱 Green IoT (1.8W Standby)
      </div>
      
      <div style="position: absolute; bottom: 16px; left: 32px; background: #ffffff; border: 1.5px solid #0f766e; padding: 8px 14px; border-radius: 20px; font-size: 12px; font-weight: 700; color: #0f766e; box-shadow: 0 2px 5px rgba(0,0,0,0.04);">
        ⚡ Green AI (Zero GPU Compute)
      </div>
      
      <div style="position: absolute; bottom: 16px; right: 32px; background: #ffffff; border: 1.5px solid #0f766e; padding: 8px 14px; border-radius: 20px; font-size: 12px; font-weight: 700; color: #0f766e; box-shadow: 0 2px 5px rgba(0,0,0,0.04);">
        📍 Area-Specific Relocation Adaptation
      </div>
      
      <div style="position: absolute; top: 22%; left: 24%; background: #ffffff; border: 1px solid #cbd5e1; padding: 6px 12px; border-radius: 16px; font-size: 11px; font-weight: 600; color: #1e3a8a;">
        ☁️ Edge + Cloud Architecture
      </div>
      
      <div style="position: absolute; bottom: 22%; right: 24%; background: #ffffff; border: 1px solid #cbd5e1; padding: 6px 12px; border-radius: 16px; font-size: 11px; font-weight: 600; color: #1e3a8a;">
        ৳ Ultra-Low-Cost ($67.27)
      </div>
    </div>
    
    <!-- Unified Central Cycle -->
    <div style="margin-top: 14px; background: #1e3a8a; border-radius: 8px; padding: 12px 20px; color: #ffffff; display: flex; justify-content: space-between; align-items: center;">
      <div style="font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: #38bdf8;">The NirmalNode Loop:</div>
      <div style="font-size: 13.5px; font-weight: 800; display: flex; gap: 12px; align-items: center;">
        <span>Sense</span> ➔ <span>Filter</span> ➔ <span>Predict</span> ➔ <span>Decide</span> ➔ <span>Purify</span> ➔ <span>Learn</span> ➔ <span>Adapt</span>
      </div>
      <div style="font-size: 11px; color: #93c5fd;">Closed-Loop Defense</div>
    </div>
  </div>
"""
add_slide("slide-19", "18. Core Contributions", "Core Contributions of NirmalNode", "Unified synthesis of the eight fundamental engineering innovations", "Summary of Novelty", slide_19_body)

print("Defining Slide 20...")
# SLIDE 20: Limitations + Future Work + Takeaway
slide_20_body = """
  <div style="width: 100%; display: flex; flex-direction: column; justify-content: space-between; height: 100%;">
    <!-- Top 3 Columns: Limitations, Future Work, Final Takeaway -->
    <div style="display: flex; gap: 16px; flex: 1;">
      <!-- Column 1: Limitations -->
      <div style="flex: 1; background: #f8fafc; border: 1.5px solid #e2e8f0; border-top: 4px solid #be123c; border-radius: 8px; padding: 14px; display: flex; flex-direction: column; justify-content: space-between;">
        <div>
          <h3 style="font-size: 14.5px; color: #be123c; margin-bottom: 8px;">Honest Limitations</h3>
          <div class="bullet-list" style="font-size: 11.5px; gap: 6px;">
            <div class="bullet-item">
              <div class="bullet-dot" style="background: #be123c;"></div>
              <div><strong>Single Bench-Scale Unit:</strong> Evaluated as an isolated prototype; multi-node factory mesh not physically deployed.</div>
            </div>
            <div class="bullet-item">
              <div class="bullet-dot" style="background: #be123c;"></div>
              <div><strong>MOS Gas Drift & Specificity:</strong> MQ sensors exhibit thermal drift and cross-sensitivity compared to reference analyzers.</div>
            </div>
            <div class="bullet-item">
              <div class="bullet-dot" style="background: #be123c;"></div>
              <div><strong>Simulation AI Stream:</strong> Primary prequential AI benchmark conducted on realistic simulation stream rather than full-year factory logging.</div>
            </div>
            <div class="bullet-item">
              <div class="bullet-dot" style="background: #be123c;"></div>
              <div><strong>Indicative BOM:</strong> Retail-quantity pricing in Dhaka; batch production economies not yet leveraged.</div>
            </div>
          </div>
        </div>
        <div style="font-size: 10.5px; color: #64748b; font-style: italic; border-top: 1px dashed #e2e8f0; padding-top: 6px;">
          Acknowledged per Chapter 4.9 limitations.
        </div>
      </div>
      
      <!-- Column 2: Future Work -->
      <div style="flex: 1; background: #f8fafc; border: 1.5px solid #e2e8f0; border-top: 4px solid #0f766e; border-radius: 8px; padding: 14px; display: flex; flex-direction: column; justify-content: space-between;">
        <div>
          <h3 style="font-size: 14.5px; color: #0f766e; margin-bottom: 8px;">Future Research Horizons</h3>
          <div class="bullet-list" style="font-size: 11.5px; gap: 6px;">
            <div class="bullet-item">
              <div class="bullet-dot"></div>
              <div><strong>Multi-Node Factory Deployment:</strong> Mesh network scaling across welding, generator, and chemical bays (Figure 3.10).</div>
            </div>
            <div class="bullet-item">
              <div class="bullet-dot"></div>
              <div><strong>Federated Learning:</strong> Nodes exchange privacy-preserving model gradient weights without leaking raw industrial data.</div>
            </div>
            <div class="bullet-item">
              <div class="bullet-dot"></div>
              <div><strong>Native Edge-AI Inference:</strong> Quantizing linear/tree models for zero-cloud ESP32 native prediction.</div>
            </div>
            <div class="bullet-item">
              <div class="bullet-dot"></div>
              <div><strong>Solar-Powered Field Variant:</strong> 20W PV panel + charge controller for off-grid operation in rural SME clusters.</div>
            </div>
          </div>
        </div>
        <div style="font-size: 10.5px; color: #0f766e; font-weight: 600; border-top: 1px dashed #e2e8f0; padding-top: 6px;">
          Roadmap for industrial translation.
        </div>
      </div>
      
      <!-- Column 3: Final Takeaway Card -->
      <div style="flex: 1; background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%); color: #ffffff; border-radius: 8px; padding: 18px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 4px 12px rgba(30, 58, 138, 0.2);">
        <div>
          <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; color: #38bdf8; letter-spacing: 1px; margin-bottom: 8px;">Core Capstone Takeaway</div>
          <p style="font-size: 15px; font-weight: 600; line-height: 1.45; color: #f8fafc;">
            "Moving industrial air quality management from passive observation to predictive, localized physical protection."
          </p>
          <p style="font-size: 12px; color: #cbd5e1; margin-top: 10px; line-height: 1.4;">
            NirmalNode demonstrates that protecting vulnerable industrial workers does not require expensive, plant-wide infrastructure—it requires <em>intelligent, adaptive, and pre-emptive hotspot action</em>.
          </p>
        </div>
        
        <div style="border-top: 1px solid rgba(255,255,255,0.15); padding-top: 10px;">
          <div style="font-size: 13px; font-weight: 800; color: #38bdf8;">Thank You!</div>
          <div style="font-size: 11px; color: #94a3b8; margin-top: 2px;">Committee Questions & Discussion</div>
        </div>
      </div>
    </div>
    
    <!-- Bottom Presenter Strip -->
    <div style="margin-top: 12px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 18px; display: flex; justify-content: space-between; align-items: center; font-size: 11.5px; color: #64748b;">
      <div><strong>Presenters:</strong> Aar Raisatunnesa Hridika & Md Rakib Hassan Dipu</div>
      <div><strong>Supervisor:</strong> Md. Ashiqussalehin (Lecturer, Dept. of IoT & Robotics Engineering)</div>
      <div><strong>University of Frontier Technology, Bangladesh</strong></div>
    </div>
  </div>
"""
add_slide("slide-20", "19. Conclusion & Discussion", "Limitations, Future Direction & Final Takeaway", "Frank assessment of prototype scope, future deployment scaling, and closing takeaway", "Conclusion & Q&A", slide_20_body)

print("Assembling HTML document...")

# Read Header and Footer from make_deck_part1
# Or construct them directly
HTML_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NirmalNode — B.Sc. Capstone Defense Presentation</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #f8fafc;
  --slide-bg: #ffffff;
  --navy: #1e3a8a;
  --navy-light: #2563eb;
  --navy-dark: #0f172a;
  --teal: #0f766e;
  --teal-light: #0d9488;
  --teal-bg: #f0fdfa;
  --emerald: #15803d;
  --emerald-light: #dcfce7;
  --amber: #b45309;
  --amber-light: #fef3c7;
  --rose: #be123c;
  --rose-light: #ffe4e6;
  --slate-50: #f8fafc;
  --slate-100: #f1f5f9;
  --slate-200: #e2e8f0;
  --slate-300: #cbd5e1;
  --slate-400: #94a3b8;
  --slate-500: #64748b;
  --slate-600: #475569;
  --slate-700: #334155;
  --slate-800: #1e293b;
  --slate-900: #0f172a;
  --font-main: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'JetBrains Mono', Consolas, monospace;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background-color: var(--bg);
  color: var(--slate-800);
  font-family: var(--font-main);
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  user-select: none;
}

#progress-bar-container {
  height: 4px;
  background: var(--slate-200);
  width: 100%;
  position: relative;
  z-index: 50;
}
#progress-bar {
  height: 100%;
  background: linear-gradient(90deg, var(--navy) 0%, var(--teal) 100%);
  width: 5%;
  transition: width 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

#presentation-container {
  flex: 1;
  position: relative;
  width: 100%;
  height: calc(100vh - 54px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px 20px;
}

.slide {
  display: none;
  width: 100%;
  max-width: 1440px;
  height: 100%;
  max-height: 820px;
  background: var(--slide-bg);
  border-radius: 12px;
  box-shadow: 0 10px 30px -5px rgba(15, 23, 42, 0.08), 0 4px 12px -2px rgba(15, 23, 42, 0.04);
  border: 1px solid var(--slate-200);
  padding: 22px 34px;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.slide.active {
  display: flex;
  animation: slideFadeIn 0.2s ease-out;
}

@keyframes slideFadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}

.slide-header {
  margin-bottom: 12px;
  border-bottom: 1.5px solid var(--slate-100);
  padding-bottom: 8px;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  flex-shrink: 0;
}

.slide-tag {
  font-size: 10.5px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  color: var(--teal);
  margin-bottom: 2px;
}

.slide-title {
  font-size: 23px;
  font-weight: 800;
  color: var(--navy);
  letter-spacing: -0.5px;
  line-height: 1.2;
}

.slide-subtitle {
  font-size: 12px;
  color: var(--slate-500);
  font-weight: 500;
  margin-top: 2px;
}

.slide-category-badge {
  background: var(--slate-100);
  color: var(--slate-600);
  font-size: 10.5px;
  font-weight: 600;
  padding: 3px 9px;
  border-radius: 20px;
  border: 1px solid var(--slate-200);
  white-space: nowrap;
}

.slide-body {
  flex: 1;
  display: flex;
  gap: 22px;
  overflow: hidden;
  align-items: stretch;
}

.col-half { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
.col-60 { flex: 6; display: flex; flex-direction: column; overflow: hidden; }
.col-40 { flex: 4; display: flex; flex-direction: column; overflow: hidden; }
.col-70 { flex: 7; display: flex; flex-direction: column; overflow: hidden; }
.col-30 { flex: 3; display: flex; flex-direction: column; overflow: hidden; }
.col-third { flex: 1; display: flex; flex-direction: column; overflow: hidden; }

#nav-bar {
  height: 50px;
  background: #ffffff;
  border-top: 1px solid var(--slate-200);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  font-size: 12.5px;
  color: var(--slate-600);
  z-index: 100;
  flex-shrink: 0;
}

.nav-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.nav-btn {
  background: var(--slate-100);
  border: 1px solid var(--slate-200);
  color: var(--slate-700);
  padding: 5px 12px;
  border-radius: 6px;
  font-size: 11.5px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: all 0.15s ease;
}

.nav-btn:hover {
  background: var(--slate-200);
  color: var(--slate-900);
}

.nav-btn.primary {
  background: var(--navy);
  color: #ffffff;
  border-color: var(--navy);
}
.nav-btn.primary:hover {
  background: var(--navy-light);
}

.slide-counter {
  font-weight: 700;
  color: var(--slate-800);
  font-variant-numeric: tabular-nums;
  background: var(--slate-100);
  padding: 3px 10px;
  border-radius: 6px;
  font-size: 12px;
  border: 1px solid var(--slate-200);
}

.img-frame {
  background: #ffffff;
  border: 1px solid var(--slate-200);
  border-radius: 8px;
  padding: 6px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  height: 100%;
}

.img-frame img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 4px;
}

.img-caption {
  font-size: 10.5px;
  color: var(--slate-500);
  text-align: center;
  margin-top: 4px;
  font-style: italic;
  flex-shrink: 0;
}

table.academic-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 11px;
  text-align: left;
}

table.academic-table th {
  background: var(--navy);
  color: #ffffff;
  font-weight: 600;
  padding: 6px 8px;
  border: 1px solid var(--navy);
  font-size: 10.5px;
  letter-spacing: 0.2px;
}

table.academic-table td {
  padding: 5px 8px;
  border-bottom: 1px solid var(--slate-200);
  color: var(--slate-800);
  vertical-align: middle;
}

table.academic-table tr:nth-child(even) {
  background: var(--slate-50);
}

table.academic-table tr.highlight-row {
  background: #fef9c3 !important;
  font-weight: 600;
}

table.academic-table tr.champion-row {
  background: #e0f2fe !important;
  font-weight: 700;
  color: var(--navy);
}

table.academic-table tr.total-row {
  background: var(--slate-100);
  border-top: 2px solid var(--navy);
  font-weight: 800;
  color: var(--navy);
  font-size: 12px;
}

.badge-2026 {
  background: #dbeafe;
  color: #1e40af;
  font-weight: 800;
  padding: 2px 5px;
  border-radius: 4px;
  font-size: 9.5px;
  border: 1px solid #bfdbfe;
  display: inline-block;
}

.kpi-row {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
  flex-shrink: 0;
}

.kpi-card {
  background: var(--slate-50);
  border: 1px solid var(--slate-200);
  border-radius: 6px;
  padding: 6px 10px;
  text-align: center;
  flex: 1;
}

.kpi-value {
  font-size: 20px;
  font-weight: 800;
  color: var(--navy);
  line-height: 1.1;
  font-variant-numeric: tabular-nums;
}

.kpi-value.green { color: var(--emerald); }
.kpi-value.teal { color: var(--teal); }
.kpi-value.amber { color: var(--amber); }

.kpi-label {
  font-size: 9.5px;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--slate-500);
  margin-top: 2px;
  letter-spacing: 0.5px;
}

.callout {
  padding: 8px 11px;
  border-radius: 6px;
  font-size: 12px;
  line-height: 1.45;
  margin-top: 6px;
}

.callout-teal {
  background: #f0fdfa;
  border-left: 3.5px solid var(--teal);
  color: #134e4a;
}

.callout-amber {
  background: #fffbeb;
  border-left: 3.5px solid var(--amber);
  color: #78350f;
}

.callout-navy {
  background: #eff6ff;
  border-left: 3.5px solid var(--navy-light);
  color: #1e3a8a;
}

.bullet-list {
  display: flex;
  flex-direction: column;
  gap: 7px;
  font-size: 12.5px;
  line-height: 1.5;
}

.bullet-item {
  display: flex;
  align-items: flex-start;
  gap: 7px;
}

.bullet-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--teal);
  margin-top: 6px;
  flex-shrink: 0;
}

.strong-term {
  font-weight: 700;
  color: var(--navy);
}

.flow-step {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 9px;
  background: var(--slate-50);
  border: 1px solid var(--slate-200);
  border-radius: 5px;
  margin-bottom: 4px;
}

.step-num {
  background: var(--navy);
  color: #ffffff;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 10px;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
  font-size: 11.5px;
}
</style>
</head>
<body>
<div id="progress-bar-container"><div id="progress-bar"></div></div>
<div id="presentation-container">
"""

HTML_FOOTER = """
</div> <!-- presentation-container -->

<div id="nav-bar">
  <div class="nav-group">
    <button class="nav-btn" id="btn-first" onclick="goToSlide(0)" title="First Slide (Home)">⏮ First</button>
    <button class="nav-btn" id="btn-prev" onclick="prevSlide()" title="Previous Slide (Left Arrow)">◀ Previous</button>
    <button class="nav-btn primary" id="btn-next" onclick="nextSlide()" title="Next Slide (Right Arrow / Space)">Next ▶</button>
    <button class="nav-btn" id="btn-last" onclick="goToSlide(totalSlides - 1)" title="Last Slide (End)">Last ⏭</button>
  </div>
  
  <div class="nav-group">
    <span class="slide-counter"><span id="current-slide-num">1</span> / <span id="total-slide-num">20</span></span>
    <button class="nav-btn" onclick="toggleFullscreen()" title="Fullscreen (F)">⛶ Fullscreen</button>
  </div>
</div>

<script>
let currentSlide = 0;
const slides = document.querySelectorAll('.slide');
const totalSlides = slides.length;
document.getElementById('total-slide-num').innerText = totalSlides;

function showSlide(index) {
  if (index < 0) index = 0;
  if (index >= totalSlides) index = totalSlides - 1;
  currentSlide = index;
  
  slides.forEach((slide, i) => {
    slide.classList.toggle('active', i === currentSlide);
  });
  
  document.getElementById('current-slide-num').innerText = currentSlide + 1;
  const pct = ((currentSlide + 1) / totalSlides) * 100;
  document.getElementById('progress-bar').style.width = pct + '%';
  
  document.getElementById('btn-prev').disabled = (currentSlide === 0);
  document.getElementById('btn-next').disabled = (currentSlide === totalSlides - 1);
}

function nextSlide() {
  if (currentSlide < totalSlides - 1) {
    showSlide(currentSlide + 1);
  }
}

function prevSlide() {
  if (currentSlide > 0) {
    showSlide(currentSlide - 1);
  }
}

function goToSlide(index) {
  showSlide(index);
}

function toggleFullscreen() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen().catch(err => alert(err.message));
  } else {
    document.exitFullscreen();
  }
}

document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
    e.preventDefault();
    nextSlide();
  } else if (e.key === 'ArrowLeft' || e.key === 'PageUp' || e.key === 'Backspace') {
    e.preventDefault();
    prevSlide();
  } else if (e.key === 'Home') {
    e.preventDefault();
    goToSlide(0);
  } else if (e.key === 'End') {
    e.preventDefault();
    goToSlide(totalSlides - 1);
  } else if (e.key.toLowerCase() === 'f') {
    e.preventDefault();
    toggleFullscreen();
  }
});

// Initialize
showSlide(0);
</script>
</body>
</html>
"""

full_html = HTML_HEAD + "".join(slides) + HTML_FOOTER

with open(out_path, "w", encoding="utf-8") as f:
    f.write(full_html)

print(f"Presentation generated successfully: {out_path}")
print(f"Total slides: {len(slides)}")
print(f"File size: {os.path.getsize(out_path):,} bytes")
