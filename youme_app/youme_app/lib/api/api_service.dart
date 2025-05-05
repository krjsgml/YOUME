import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/item_location.dart';
import '../models/team_member.dart';
import '../models/usage_history.dart';

final String baseUrl = 'http://192.168.50.96:5000/api';

class ApiService {
  Future<List<ItemLocation>> fetchItemLocations() async {
    final response = await http.get(Uri.parse('$baseUrl/item_locations'));
    if (response.statusCode == 200) {
      List jsonResponse = json.decode(response.body);
      return jsonResponse.map((item) => ItemLocation.fromJson(item)).toList();
    } else {
      throw Exception('Failed to load item locations');
    }
  }

  Future<void> addItemLocation(String name, String location, int quantity) async {
    final response = await http.post(
      Uri.parse('$baseUrl/item_locations'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'name': name, 'location': location, 'quantity': quantity}),
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to add item location');
    }
  }

  Future<void> updateItemLocation(int id, String name, String location, int quantity) async {
    final response = await http.put(
      Uri.parse('$baseUrl/item_locations/$id'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'name': name, 'location': location, 'quantity': quantity}),
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to update item location');
    }
  }

  Future<void> deleteItemLocation(int id) async {
    final response = await http.delete(Uri.parse('$baseUrl/item_locations/$id'));
    if (response.statusCode != 200) {
      throw Exception('Failed to delete item location');
    }
  }

  Future<List<TeamMember>> fetchTeamMembers() async {
    final response = await http.get(Uri.parse('$baseUrl/team_members'));
    if (response.statusCode == 200) {
      List jsonResponse = json.decode(response.body);
      return jsonResponse.map((item) => TeamMember.fromJson(item)).toList();
    } else {
      throw Exception('Failed to load team members');
    }
  }

  Future<void> addTeamMember(String name, String phone, String position) async {
    final response = await http.post(
      Uri.parse('$baseUrl/team_members'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'name': name, 'phone_number': phone, 'position': position}),
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to add team member');
    }
  }

  Future<void> updateTeamMember(int id, String name, String phone, String position) async {
    final response = await http.put(
      Uri.parse('$baseUrl/team_members/$id'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'name': name, 'phone_number': phone, 'position': position}),
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to update team member');
    }
  }

  Future<void> deleteTeamMember(int id) async {
    final response = await http.delete(Uri.parse('$baseUrl/team_members/$id'));
    if (response.statusCode != 200) {
      throw Exception('Failed to delete team member');
    }
  }

  Future<List<UsageHistory>> fetchUsageHistories({int? id, String? date}) async {
    String query = '';
    if (id != null) query += '?id=$id';
    if (date != null) query += (query.isEmpty ? '?' : '&') + 'date=$date';

    final response = await http.get(Uri.parse('$baseUrl/usage_histories$query'));
    if (response.statusCode == 200) {
      List jsonResponse = json.decode(response.body);
      return jsonResponse.map((item) => UsageHistory.fromJson(item)).toList();
    } else {
      throw Exception('Failed to load usage histories');
    }
  }
}
