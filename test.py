try:
    with open('key.txt', 'r') as f:
        api_key = f.read().splitlines()
except:
    print("Can't read api key. Create key.txt file and paste api_key there.")
    exit(7)



print(api_key)