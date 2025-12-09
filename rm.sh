echo "Will Delete（共 $(docker images "swebench/*" -q | sort -u | wc -l) 个）："
docker images "swebench/*" --format "table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.Size}}\t{{.CreatedSince}}" | nl

read -p "(y/N) " confirm
if [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]]; then
    docker rmi -f $(docker images "swebench/*" -q | sort -u)
    echo "Done"
else
    echo "Done"
fi