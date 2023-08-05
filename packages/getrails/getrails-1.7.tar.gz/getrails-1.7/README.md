<center>
  <img src="https://github.com/Jul10l1r4/getrailslib/img/beta1.jpg" alt="Getrails" width="900px"/>
</center>

![Upload Python Package](https://github.com/Jul10l1r4/getrailslib/workflows/Upload%20Python%20Package/badge.svg?branch=lib)

# GETRAILS
Lib of OSINT and Dork hacking that work with Google and Duckduckgo

## Run

```python
import getrails
getrails.search('site:scanme.nmap.org')) # Try Google search if return error use Duckduckgo
# ["http://scanme.nmap.org",...]

getrails.go_gle("term") # Searching Google
getrails.go_duck("term") # Searching Duckduckgo
```

## Install

```pypi
pip3 install getrails
```
