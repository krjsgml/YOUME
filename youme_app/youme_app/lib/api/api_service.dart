import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/item_location.dart';
import '../models/team_member.dart';
import '../models/usage_history.dart';

class ApiService {
  final String baseUrl = 'http://your-api-endpoint'; // ← 여기 본인 API 주소로 수정하세요

  // Item Location 가져오기
  Future<List<ItemLocation>> fetchItemLocation() async {
    final response = await http.get(Uri.parse('$baseUrl/item_location'));

    if (response.statusCode == 200) {
      List<dynamic> data = json.decode(response.body);
      return data.map((item) => ItemLocation.fromJson(item)).toList();
    } else {
      throw Exception('Failed to load item locations');
    }
  }

  // Team Member 가져오기
  Future<List<TeamMember>> fetchTeamMember() async {
    final response = await http.get(Uri.parse('$baseUrl/team_member'));

    if (response.statusCode == 200) {
      List<dynamic> data = json.decode(response.body);
      return data.map((item) => TeamMember.fromJson(item)).toList();
    } else {
      throw Exception('Failed to load team members');
    }
  }

  // Usage History 가져오기
  Future<List<UsageHistory>> fetchUsageHistory() async {
    final response = await http.get(Uri.parse('$baseUrl/usage_history'));

    if (response.statusCode == 200) {
      List<dynamic> data = json.decode(response.body);
      return data.map((item) => UsageHistory.fromJson(item)).toList();
    } else {
      throw Exception('Failed to load usage history');
    }
  }
}
