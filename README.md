# 2023Synthesis-group2-roof

## Used data: 10-248-560.city.json
## project workflow log
https://docs.google.com/document/d/1YOHux7onHhxHejFOVWln2l9hKwplqT__alUNZnTUp_o/

## code link
1. roof feature calculation(area, MaxAngle,MinAngle,Num_polygon,MaxAreaPropotion,LargestPolygonAngle)
[format transfer and roof features](https://colab.research.google.com/drive/1ZtcIgcoYbqEVTBzJMiFyZfM6C4SUQfPe?usp=sharing)
2.building neighbour feature & roof extraction
https://colab.research.google.com/drive/11FLiN5p4gI0AK2H6m-7nWrZMexECgOKl#scrollTo=ayMxLHyJiUwm
3.3dmetrics
- Colab code
[feature selection](https://colab.research.google.com/drive/1YQhWCa7Axx41Sl73Isk6hnVwzsV65Xan?usp=sharing#scrollTo=jue9294f0pIK)
- **working directory-Chengzhi's Google drive**, shared already
https://drive.google.com/drive/folders/1waKB7Fu_7dkqTSEeJmUSNJ5C2i5kcdJs?usp=sharing

## Meeting material
[kickoff meeting](https://docs.google.com/presentation/d/1enXZU5XdtqdpiU2tukcHxfAW6W4gz8qLLUbAWUPvkdQ/edit#slide=id.p), *including some resources and papers*


-------------------------------------------------------------
### server
**For Windows**
ssh -fNg -L 5433:localhost:5432 -o ProxyCommand="ssh.exe -i c:/Users/<username>/.ssh/know_hosts -W %h:%p netid@linux-bastion-ex.tudelft.nl" dbusername@godzilla.bk.tudelft.nl 

ssh netid@student-linux.tudelft.nl
netid password

ssh username@godzilla.bk.tudelft.nl
server password

- Open DBdeaver
- create a new connection, follow the instruction
- edit connection, click "all the database"
