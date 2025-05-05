import 'package:flutter/material.dart';
import 'package:youme_app/api/api_service.dart';
import 'package:youme_app/models/item_location.dart';

class ItemLocationScreen extends StatefulWidget {
  @override
  _ItemLocationScreenState createState() => _ItemLocationScreenState();
}

class _ItemLocationScreenState extends State<ItemLocationScreen> {
  late Future<List<ItemLocation>> futureItemLocations;

  // TextEditingController 선언
  final TextEditingController itemNameController = TextEditingController();
  final TextEditingController locationController = TextEditingController();
  final TextEditingController quantityController = TextEditingController();

  @override
  void initState() {
    super.initState();
    futureItemLocations = ApiService().fetchItemLocations();  // API 호출
  }

  // 새로운 아이템 추가
  void _addItemLocation() {
    itemNameController.clear();
    locationController.clear();
    quantityController.clear();
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: Text('Add Item Location'),
          content: Column(
            children: [
              TextField(
                controller: itemNameController,
                decoration: InputDecoration(labelText: 'Item Name'),
              ),
              TextField(
                controller: locationController,
                decoration: InputDecoration(labelText: 'Location'),
              ),
              TextField(
                controller: quantityController,
                decoration: InputDecoration(labelText: 'Quantity'),
              ),
            ],
          ),
          actions: <Widget>[
            TextButton(
              onPressed: () {
                String itemName = itemNameController.text;
                String location = locationController.text;
                int quantity = int.tryParse(quantityController.text) ?? 0;

                ApiService().addItemLocation(itemName, location, quantity).then((_) {
                  setState(() {
                    futureItemLocations = ApiService().fetchItemLocations(); // 아이템 추가 후 UI 새로 고침
                  });
                  Navigator.pop(context);  // 다이얼로그 닫기
                });
              },
              child: Text('Add'),
            ),
          ],
        );
      },
    );
  }

  // 아이템 삭제
  void _deleteItemLocation(int id) {
    ApiService().deleteItemLocation(id).then((_) {
      setState(() {
        futureItemLocations = ApiService().fetchItemLocations();  // 삭제 후 UI 갱신
      });
    });
  }

  // 아이템 수정
  void _editItemLocation(ItemLocation item) {
    itemNameController.text = item.name;
    locationController.text = item.location;
    quantityController.text = item.quantity.toString();

    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: Text('Edit Item Location'),
          content: Column(
            children: [
              TextField(
                controller: itemNameController,
                decoration: InputDecoration(labelText: 'Item Name'),
              ),
              TextField(
                controller: locationController,
                decoration: InputDecoration(labelText: 'Location'),
              ),
              TextField(
                controller: quantityController,
                decoration: InputDecoration(labelText: 'Quantity'),
              ),
            ],
          ),
          actions: <Widget>[
            TextButton(
              onPressed: () {
                String itemName = itemNameController.text;
                String location = locationController.text;
                int quantity = int.tryParse(quantityController.text) ?? 0;

                ApiService().updateItemLocation(item.id, itemName, location, quantity).then((_) {
                  setState(() {
                    futureItemLocations = ApiService().fetchItemLocations();  // 수정 후 UI 갱신
                  });
                  Navigator.pop(context);  // 다이얼로그 닫기
                });
              },
              child: Text('Save'),
            ),
          ],
        );
      },
    );
  }

  Map<String, List<ItemLocation>> _groupItemLocationsByLocation(List<ItemLocation> itemLocations) {
    Map<String, List<ItemLocation>> groupedLocations = {};
    for (var item in itemLocations) {
      if (groupedLocations.containsKey(item.location)) {
        groupedLocations[item.location]!.add(item);
      } else {
        groupedLocations[item.location] = [item];
      }
    }
    return groupedLocations;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Item Location"),
        automaticallyImplyLeading: false,
        leading: IconButton(
          icon: Icon(Icons.arrow_back),
          onPressed: () {
            Navigator.pop(context);
          },
        ),
      ),
      body: FutureBuilder<List<ItemLocation>>(
        future: futureItemLocations,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          } else if (snapshot.hasData) {
            List<ItemLocation> itemLocations = snapshot.data!;
            Map<String, List<ItemLocation>> groupedLocations = _groupItemLocationsByLocation(itemLocations);

            return ListView.builder(
              itemCount: groupedLocations.keys.length,
              itemBuilder: (context, index) {
                String location = groupedLocations.keys.elementAt(index);
                List<ItemLocation> itemsInLocation = groupedLocations[location]!;

                return Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Card(
                    elevation: 5,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: ExpansionTile(
                      title: Text(
                        location,
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 18,
                        ),
                      ),
                      children: itemsInLocation.map((item) {
                        return ListTile(
                          title: Text(item.name),
                          subtitle: Text("Quantity: ${item.quantity}"),
                          leading: Icon(Icons.location_on),
                          trailing: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              IconButton(
                                icon: Icon(Icons.edit),
                                onPressed: () => _editItemLocation(item),
                              ),
                              IconButton(
                                icon: Icon(Icons.delete),
                                onPressed: () => _deleteItemLocation(item.id),
                              ),
                            ],
                          ),
                        );
                      }).toList(),
                    ),
                  ),
                );
              },
            );
          } else {
            return Center(child: Text("No data available"));
          }
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _addItemLocation,
        child: Icon(Icons.add),
      ),
    );
  }
}
