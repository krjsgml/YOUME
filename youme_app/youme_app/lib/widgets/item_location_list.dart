import 'package:flutter/material.dart';
import 'package:youme_app/models/item_location.dart';
import 'package:youme_app/api/api_service.dart';

class ItemLocationList extends StatelessWidget {
  final List<ItemLocation> itemLocations;

  ItemLocationList({required this.itemLocations});

  void _deleteItemLocation(int id) {
    ApiService().deleteItemLocation(id);
    // 삭제 후 UI 새로고침
  }

  void _editItemLocation(ItemLocation itemLocation) {
    // 아이템 수정 화면
  }

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: itemLocations.length,
      itemBuilder: (context, index) {
        final item = itemLocations[index];
        return ListTile(
          title: Text(item.name),
          subtitle: Text("Location: ${item.location}, Quantity: ${item.quantity}"),
          onTap: () => _editItemLocation(item),  // 아이템 클릭 시 수정 화면으로 이동
          trailing: IconButton(
            icon: Icon(Icons.delete),
            onPressed: () => _deleteItemLocation(item.id),  // 아이템 삭제
          ),
        );
      },
    );
  }
}
