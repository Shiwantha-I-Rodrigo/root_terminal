# ROOT TERMINAL

## VIDEO PRODUCTION PROCESS

**Install Manim**
```
sudo pacman -Syu base-devel cairo pango
sudo pacman -S texlive-basic texlive-latex texlive-latexrecommended texlive-latexextra texlive-fontsrecommended texlive-mathscience
```
**Start a Manim Project**
```
python -m venv env
source env/bin/activate
manim init project my-project --default
```
- *example manim project*
    ```
    from manim import *
    class CreateCircle(Scene):
        def construct(self):
            circle = Circle()
            circle.set_fill(PINK, opacity=0.5)
            self.play(Create(circle))
    ```
**Export Manim Video**
```
manim -pql circle_animation.py CreateCircle # preview
manim -pqh circle_animation.py CreateCircle # hq render
```
**Install Asciinema / Ascinema-agg** (CLI Recorder)
```
sudo pacman -Syu ascinema
yay -S agg ascinema-agg
```
**Record CLI Actions**
```
asciinema rec demo.cast
asciinema play demo.cast 
```
**Export Recording to gif**
```
agg demo.cast demo.gif
```
**Install MoviePy**
```
pip install moviepy
```

**Upscale videos to match MANIM output**
```
ffmpeg -i input_720p.mp4 \
    -vf "scale=1920:1080:flags=lanczos,format=yuv420p" \
    -r 30 -c:v libx264 -preset slow -crf 18 -c:a copy \
    output_1080p.mp4
```

**Merging the Videos**

```
#inputs.txt
file 'manim_intro.mp4'
file 'upscaled_720p_content.mp4'
file 'manim_outro.mp4'
```

```
ffmpeg -f concat -safe 0 -i inputs.txt -c copy final_video.mp4
```

### CCNA Crash Course

| Video | Title | Description (Keywords & Objectives) |
| :--- | :--- | :--- |
| **01** | **Network Components & Architecture** | **Explain** the role/function of routers, L2/L3 switches, Next-Gen Firewalls/IPS, APs, Controllers (WLC/DNA Center), and **PoE**. **Describe** 2-tier, 3-tier, Spine-leaf, SOHO, and On-prem vs. Cloud architectures. |
| **02** | **Physical Layer & Ethernet** | **Compare** single-mode/multimode fiber and copper. **Identify** interface/cable issues (collisions, errors, duplex/speed mismatch). **Compare** TCP vs. UDP. |
| **03** | **IPv4 & Subnetting Mastery** | **Configure and Verify** IPv4 addressing and subnetting (Public/Private). Master CIDR notation and VLSM. |
| **04** | **IPv6: The Next Generation** | **Configure and Verify** IPv6 addressing/prefixes. **Describe** IPv6 address types: Global Unicast, Unique Local, Link-Local, Anycast, Multicast, and Modified EUI-64. |
| **05** | **Switching Fundamentals & CLI** | **Describe** MAC learning/aging, frame switching, flooding, and MAC tables. **Configure and Verify** basic CLI, hostnames, and passwords. |
| **06** | **VLANs & Discovery Protocols** | **Configure and Verify** VLANs (data/voice, default, native), inter-VLAN connectivity, and L2 discovery via **CDP** and **LLDP**. |
| **07** | **Rapid PVST+ & STP Hardening** | **Interpret** STP operations (Root bridge, port states/roles). **Interpret** advanced features: **Root guard, Loop guard, BPDU filter, and BPDU guard**. |
| **08** | **Aggregating Links: EtherChannel** | **Configure and Verify** Layer 2 and Layer 3 EtherChannel using **LACP**. |
| **09** | **Routing Tables & Forwarding** | **Interpret** routing table components (Prefix, mask, next hop, AD, metric, gateway of last resort). **Determine** forwarding decisions via Longest Prefix Match. |
| **10** | **Static Routing (IPv4 & IPv6)** | **Configure and Verify** Default, Network, Host, and **Floating Static** routes. |
| **11** | **Dynamic Routing: OSPFv2** | **Configure and Verify** single-area OSPFv2 (Neighbor adjacencies, point-to-point, broadcast DR/BDR, and Passive interfaces). |
| **12** | **First Hop Redundancy (FHRP)** | **Describe** the purpose and concepts of FHRP, specifically focusing on **HSRP** operations. |
| **13** | **IP Services: DHCP, DNS, & NTP** | **Configure and Verify** DHCP (client/relay/DORA) and NTP (client/server). **Explain** the roles of DNS, TFTP, and FTP in the network. |
| **14** | **Monitoring & Network Ops** | **Explain** SNMP (versions/messages). **Describe** Syslog features (facilities and levels). **Describe** cloud-managed device access. |
| **15** | **Traffic Management: QoS** | **Explain** forwarding PHB for QoS: **Classification, Marking, Queuing, Congestion, Policing, and Shaping**. |
| **16** | **The Masquerade: NAT & PAT** | **Configure and Verify** inside source NAT using static and pools (Overload/PAT). |
| **17** | **Access Control Lists (ACLs)** | **Configure and Verify** standard and extended ACLs using permit/deny logic and wildcard masks. |
| **18** | **Layer 2 Security Features** | **Configure and Verify** **Port Security**, **DHCP Snooping**, and **Dynamic ARP Inspection (DAI)**. |
| **19** | **VPNs & Security Fundamentals** | **Describe** IPsec remote access and site-to-site **VPNs**. **Compare** AAA concepts. **Describe** MFA, certificates, and biometrics. |
| **20** | **Wireless: WLCs & Security** | **Describe** Wireless architectures and AP modes. **Describe** security protocols (**WPA/WPA2/WPA3**). **Configure** WLAN via GUI with WPA2 PSK. |
| **21** | **Virtualization & SD-Access** | **Explain** Virtualization, **Containers**, and **VRFs**. **Describe** SDA architecture (Overlay, Underlay, Fabric, Northbound/Southbound APIs). |
| **22** | **The AI & Automation Era** | **Explain AI (Generative and Predictive)** and **Machine Learning** in ops. **Recognize** capabilities of **Ansible** and **Terraform** (Puppet/Chef removed). |
| **23** | **APIs & JSON Data** | **Describe** REST-based APIs (CRUD, HTTP verbs, auth types). **Recognize** components of **JSON-encoded data**. |
| **24** | **Final Review & Exam Day** | High-level recap of all 6 domains. Strategy for **Performance-Based Labs**, Drag-and-Drop, and Multiple Choice questions. |

### Important Notes :
*  **"Configure and Verify"** = video should include a hands-on lab demonstration.
*  **"Explain"** / **"Describe,"**  = conceptual animations or slides.
*  **AI Focus:** For Video 22, focus only on how AI/ML assists in network troubleshooting and predictive maintenance.
*  **Infrastructure as Code:**  = Ensure to emphasize **Terraform** over the now-removed Puppet.
