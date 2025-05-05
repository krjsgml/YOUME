import 'package:flutter/material.dart';
import 'package:youme_app/models/team_member.dart';

class MemberList extends StatelessWidget {
  final List<TeamMember> members;
  final Function(int id) onDelete;
  final Function(int id, String name, String phone, String position) onEdit;
  final Function(String name, String phone, String position) onAdd;

  MemberList({
    required this.members,
    required this.onDelete,
    required this.onEdit,
    required this.onAdd,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Expanded(
          child: ListView.builder(
            itemCount: members.length,
            itemBuilder: (context, index) {
              final member = members[index];
              return ListTile(
                title: Text(member.name),
                subtitle: Text('${member.position} - ${member.phoneNumber}'),
                trailing: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    IconButton(
                      icon: Icon(Icons.edit),
                      onPressed: () {
                        _showEditDialog(context, member);
                      },
                    ),
                    IconButton(
                      icon: Icon(Icons.delete),
                      onPressed: () => onDelete(member.id),
                    ),
                  ],
                ),
              );
            },
          ),
        ),
        Padding(
          padding: EdgeInsets.all(8.0),
          child: ElevatedButton(
            onPressed: () {
              _showAddDialog(context);
            },
            child: Text("Add Member"),
          ),
        ),
      ],
    );
  }

  void _showAddDialog(BuildContext context) {
    String name = '';
    String phone = '';
    String position = '';

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text("Add Member"),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              decoration: InputDecoration(labelText: 'Name'),
              onChanged: (value) => name = value,
            ),
            TextField(
              decoration: InputDecoration(labelText: 'Phone'),
              onChanged: (value) => phone = value,
            ),
            TextField(
              decoration: InputDecoration(labelText: 'Position'),
              onChanged: (value) => position = value,
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(context);
            },
            child: Text("Cancel"),
          ),
          ElevatedButton(
            onPressed: () {
              onAdd(name, phone, position);
              Navigator.pop(context);
            },
            child: Text("Add"),
          ),
        ],
      ),
    );
  }

  void _showEditDialog(BuildContext context, TeamMember member) {
    String name = member.name;
    String phone = member.phoneNumber;
    String position = member.position;

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text("Edit Member"),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              decoration: InputDecoration(labelText: 'Name'),
              controller: TextEditingController(text: name),
              onChanged: (value) => name = value,
            ),
            TextField(
              decoration: InputDecoration(labelText: 'Phone'),
              controller: TextEditingController(text: phone),
              onChanged: (value) => phone = value,
            ),
            TextField(
              decoration: InputDecoration(labelText: 'Position'),
              controller: TextEditingController(text: position),
              onChanged: (value) => position = value,
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(context);
            },
            child: Text("Cancel"),
          ),
          ElevatedButton(
            onPressed: () {
              onEdit(member.id, name, phone, position);
              Navigator.pop(context);
            },
            child: Text("Save"),
          ),
        ],
      ),
    );
  }
}
