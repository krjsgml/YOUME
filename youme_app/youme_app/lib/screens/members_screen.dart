import 'package:flutter/material.dart';
import 'package:youme_app/api/api_service.dart';
import 'package:youme_app/models/team_member.dart';
import 'package:youme_app/widgets/member_list.dart';

class MembersScreen extends StatefulWidget {
  @override
  _MembersScreenState createState() => _MembersScreenState();
}

class _MembersScreenState extends State<MembersScreen> {
  late Future<List<TeamMember>> members;

  @override
  void initState() {
    super.initState();
    members = ApiService().fetchTeamMembers();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Team Members"),
        automaticallyImplyLeading: true,
      ),
      body: FutureBuilder<List<TeamMember>>(
        future: members,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text("Error: ${snapshot.error}"));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return Center(child: Text("No members found"));
          } else {
            return MemberList(
              members: snapshot.data!,
              onDelete: _deleteMember,
              onEdit: _editMember,
              onAdd: _addMemberCallback,  // ✅ 추가된 부분
            );
          }
        },
      ),
    );
  }

  void _addMemberCallback(String name, String phone, String position) async {
    await ApiService().addTeamMember(name, phone, position);
    setState(() {
      members = ApiService().fetchTeamMembers();
    });
  }

  void _deleteMember(int id) async {
    await ApiService().deleteTeamMember(id);
    setState(() {
      members = ApiService().fetchTeamMembers();
    });
  }

  void _editMember(int id, String name, String phone, String position) async {
    await ApiService().updateTeamMember(id, name, phone, position);
    setState(() {
      members = ApiService().fetchTeamMembers();
    });
  }
}
