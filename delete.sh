# echo $1
torrent_id=`transmission-remote -n 'anyjava:gusxo0410' -l | fgrep "$1" | awk '{print $1}'`

if [ "$torrent_id" = "" ] 
then
  echo $torrent_id / $1 torrent is not exists.
  exit 1
fi

transmission-remote -n 'anyjava:gusxo0410' -t $torrent_id --remove-and-delete

