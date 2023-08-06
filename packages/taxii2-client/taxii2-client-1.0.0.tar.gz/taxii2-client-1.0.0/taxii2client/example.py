import taxii2client
from taxii2client.v20 import as_pages
collection = taxii2client.Collection("http://localhost:5000/trustgroup1/collections/91a7b528-80eb-42ed-a74d-c6fbd5a26116/", user="admin", password="Password0")

# bundle = collection.get_objects(per_request=77)
# for bundle in collection.get_objects():
# print(len(bundle["objects"]), bundle)

# for bundle in as_pages(collection.get_objects, per_request=77):
#     print(len(bundle["objects"]), bundle)

for bundle in as_pages(collection.get_manifest, per_request=77, **{"type": "indicator"}):
    print(len(bundle["objects"]), bundle)

bundle = collection.get_objects()
print(len(bundle["objects"]), bundle)
