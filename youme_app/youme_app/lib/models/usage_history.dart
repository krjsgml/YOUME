class UsageHistory {
  final int usageNum;
  final int id;
  final String name;
  final String robotId;
  final DateTime? startTime;
  final DateTime? stopTime;
  final DateTime? usageDate;

  UsageHistory({
    required this.usageNum,
    required this.id,
    required this.name,
    required this.robotId,
    this.startTime,
    this.stopTime,
    this.usageDate,
  });

  factory UsageHistory.fromJson(Map<String, dynamic> json) {
    return UsageHistory(
      usageNum: json['usage_num'],
      id: json['id'],
      name: json['name'] ?? '',
      robotId: json['robot_id'] ?? '',
      startTime: json['start_time'] != null ? DateTime.tryParse(json['start_time']) : null,
      stopTime: json['stop_time'] != null ? DateTime.tryParse(json['stop_time']) : null,
      usageDate: json['usage_date'] != null ? DateTime.tryParse(json['usage_date']) : null,
    );
  }
}
