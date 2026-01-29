# DanZens
**Official GitHub repository for the IEEE PerCom 2025 demo paper**

DanZens is a toolkit for real-time motion analysis in dance using wearable sensors. By combining motion capture, annotation, and visualization, it enables precise, cost-effective comparisons between two performers.

The system was developed as part of an IEEE PerCom 2025 demo paper and was presented live at the conference, demonstrating its real-world applicability in both research and interactive settings.

DanZens leverages Sony Mocopi sensors, DanceTag for movement capture, and DanceVis for visualizing performance differences using Dynamic Time Warping (DTW). The system provides actionable, personalized feedback without requiring expensive lab-based equipment.

## Features
- **Wearable sensor integration:** captures detailed movement data in real time.
- **Annotation pipeline:** DanceTag allows easy tagging of movements for comparison.
- **Visual feedback:** DanceVis generates intuitive heat maps to highlight differences in performance.
- **Dynamic Time Warping:** compares sequences of movements for precise similarity analysis.
- **Accessible & cost-effective:** no specialized biomechanical equipment needed.
- **Post-capture feedback:** designed to enhance learning and practice in dance.
  
## Technology
- **Sensors:** Sony Mocopi
- **Algorithms:** Dynamic Time Warping (DTW) for motion comparison
- **Languages/Tools:** Python, data visualization libraries (Matplotlib/Seaborn), real-time data processing libraries
- **Pipeline:** Sensor input → Capture → Annotation → DTW comparison → Heatmap visualization

## Paper / Reference
Y. Mego, C. Valdez, H. M. Camarillo-Abad, and F. L. Cibrian, “DanZens: Wearable Technology for Real-Time Motion Analysis in Dance,” in *Proc. IEEE Int. Conf. Pervasive Computing and Communications (PerCom)*, 2025. [Online]. Available: https://ieeexplore.ieee.org/document/11038673

## Funding
This work was supported by an Undergraduate Research Grant from Chapman University.  
Conference travel was supported by the Fowler School of Engineering and the Center for Undergraduate Excellence at Chapman University.
