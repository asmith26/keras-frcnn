floyd run --gpu \
          --data tZeJYHomF4FLE5TkbXP8rJ:test1_data \
          --data pZ85WaK3gwUbzLdkfCjnse:models \
          --env tensorflow:py2 \
          "python test_frcnn.py --path=/test1_data/"

# floyd status
# floyd logs AKpnXqj9BEU6d8KhmygTyb -t
