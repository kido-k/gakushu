https://qiita.com/phorizon20/items/57277fab1fd7aa994502

mkdir Dockerfile

Dockerfile
-----------------
FROM ubuntu:latest

RUN apt-get update
RUN apt-get install python3 python3-pip -y

RUN pip3 install flask
-----------------

// dockerfileのビルド
docker build . -t python/flask:1.0

// ビルドしたコンテナに入る時のコマンド
docker run -it python/flask:1.0 /bin/bash

// dockerコンテナの状態を確認
docker ps -a

// dockerコンテナの起動と停止
docker start <container id>
docker stop <container id>

// dockerコンテナで5000番ポートでsrcフォルダをマウントしてコマンド実行
docker run -it -p 5000:5000 -v $(pwd)/src:/src python/flask:1.0 /bin/bash