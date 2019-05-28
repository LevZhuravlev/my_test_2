# https://stackoverflow.com/questions/23935141/how-to-copy-docker-images-from-one-host-to-another-without-using-a-repository
docker save apalkoff/botan | bzip2 | pv | ssh root@uniyar_bot.apalkoff.ru 'bunzip2 | docker load'
scp docker-compose.yml root@uniyar_bot.apalkoff.ru:~
ssh root@uniyar_bot.apalkoff.ru 'docker-compose up -d --no-deps botan '
