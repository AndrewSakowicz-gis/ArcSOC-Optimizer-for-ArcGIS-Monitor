<div align="center">
  <h3 align="center">ArcSOC Optimizer for ArcGIS Monitor</h3>
</div>

  
## Contents

- [Contents](#contents)
- [About](#about)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [Contact](#contanct)


  
## About
ArcSOC Optimizer can help administrators:
1.	Reduce memory by identifying low usage services with dedicated pooling and reducing the overall number of arcsoc.exe processes: 
a.	changing dedicated to shared instance pool, if supported   
b.	reducing min instances for dedicated instance pool services
2.	Improve performance by identifying high usage service and allocating dedicated arcsoc.exe processes if available memory:
a.	changing shared to dedicated instance pool
b.	increasing min instances for dedicated instance pool

See User Guide in the documentation folder.

  
## Getting Started
To run using provided executable for windows, unzip ArcSOCOptimizer.zip from the latest Release https://github.com/EsriPS/arcgis-monitor-arcsoc-optimizer/releases, go to dist folder and execute from command line:
```shell
ArcSOCOptimizer.exe -f sampleConfig.json
```
To run as python script:
```shell
pip install -r requirements.txt
ArcSOCOptimizer.py -f sampleConfig.json
```
To build executable for your environment:
```shell
pip install -r requirements.txt
pyinstaller.exe ArcSOCOptimizer.py --onefile
```
 
## Contributing

We welcome pull requests from anyone! If you're interested in contributing to this project, check out [CONTRIBUTING.md](CONTRIBUTING.md).

## Contact
If you're looking for more info about this project, please contact asakowicz@esri.com

