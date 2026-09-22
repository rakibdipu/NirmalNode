with open(r'c:\Users\ASUS\Downloads\capstone 3.2\build_full_presentation.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace image in HTML generator
code = code.replace(
    'src="extracted_figs/five_layer_architecture.png"',
    'src="figures_academic/five_layer_architecture_academic.png"'
)

# Replace table in Slide 4
old_html_table = """        <tr class="highlight-row">
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
        </tr>"""

new_html_table = """        <tr class="highlight-row">
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
        </tr>"""

code = code.replace(old_html_table, new_html_table)

with open(r'c:\Users\ASUS\Downloads\capstone 3.2\build_full_presentation.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated build_full_presentation.py successfully.")
