![Getrails](img/beta1.jpg)

![Upload Python Package](workflows/Upload%20Python%20Package/badge.svg?branch=master)

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
