![Getrails](img/banner.png)

# GETRAILS

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/403eac2b51ef4546a1170720dfb46f1f)](https://app.codacy.com/manual/Jul10l1r4/getrails?utm_source=github.com&utm_medium=referral&utm_content=Jul10l1r4/getrails&utm_campaign=Badge_Grade_Dashboard)

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
