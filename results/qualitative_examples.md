# Qualitative Examples

## Correct

- Source: `functiongemma-zero-shot.jsonl` / ID: `mobile-actions-008696`
  - Command: Please set up a new calendar event for 'Team Lunch with Marketing' on May 13, 2025 at 1:30 PM.
  - Gold: `{"name": "create_calendar_event", "arguments": {"title": "Team Lunch with Marketing", "datetime": "2025-05-13T13:30:00"}, "raw": {"name": "create_calendar_event", "arguments": {"title": "Team Lunch with Marketing", "datetime": "2025-05-13T13:30:00"}}, "parse_error": null}`
  - Prediction: `{"name": "create_calendar_event", "arguments": {"datetime": "2025-05-13T13:30:00", "title": "Team Lunch with Marketing"}, "raw": {"name": "create_calendar_event", "arguments": {"datetime": "2025-05-13T13:30:00", "title": "Team Lunch with Marketing"}}, "parse_error": null}`

- Source: `functiongemma-zero-shot.jsonl` / ID: `mobile-actions-008698`
  - Command: Turn on the flashlight and show me the location of the Sunnyvale Library on the map.
  - Gold: `{"name": "turn_on_flashlight", "arguments": {}, "raw": {"name": "turn_on_flashlight", "arguments": {}}, "parse_error": null}`
  - Prediction: `{"name": "turn_on_flashlight", "arguments": {}, "raw": {"name": "turn_on_flashlight", "arguments": {}}, "parse_error": null}`

- Source: `functiongemma-zero-shot.jsonl` / ID: `mobile-actions-008701`
  - Command: Please schedule a calendar event titled 'Quarterly Budget Review' for 10:30 AM on Thursday, June 20th, and also send an email to rsharma@financelink.co.in with the subject 'Budget Meeting Invite' and the body 'Please see the calendar invite for the quarterly review. Bring the Q2 expenditure reports.'
  - Gold: `{"name": "create_calendar_event", "arguments": {"title": "Quarterly Budget Review", "datetime": "2024-06-20T10:30:00"}, "raw": {"name": "create_calendar_event", "arguments": {"title": "Quarterly Budget Review", "datetime": "2024-06-20T10:30:00"}}, "parse_error": null}`
  - Prediction: `{"name": "create_calendar_event", "arguments": {"datetime": "2024-06-20T10:30:00", "title": "Quarterly Budget Review"}, "raw": {"name": "create_calendar_event", "arguments": {"datetime": "2024-06-20T10:30:00", "title": "Quarterly Budget Review"}}, "parse_error": null}`

- Source: `functiongemma-zero-shot.jsonl` / ID: `mobile-actions-008702`
  - Command: I need to check under the sofa, please turn on the flashlight.
  - Gold: `{"name": "turn_on_flashlight", "arguments": {}, "raw": {"name": "turn_on_flashlight", "arguments": {}}, "parse_error": null}`
  - Prediction: `{"name": "turn_on_flashlight", "arguments": {}, "raw": {"name": "turn_on_flashlight", "arguments": {}}, "parse_error": null}`

- Source: `functiongemma-zero-shot.jsonl` / ID: `mobile-actions-008704`
  - Command: Can you show me where The Wandering Page bookstore is located in Brooklyn?
  - Gold: `{"name": "show_map", "arguments": {"query": "The Wandering Page bookstore in Brooklyn"}, "raw": {"name": "show_map", "arguments": {"query": "The Wandering Page bookstore in Brooklyn"}}, "parse_error": null}`
  - Prediction: `{"name": "show_map", "arguments": {"query": "The Wandering Page bookstore in Brooklyn"}, "raw": {"name": "show_map", "arguments": {"query": "The Wandering Page bookstore in Brooklyn"}}, "parse_error": null}`

## Parse Error

- Source: `babyA-eval.jsonl` / ID: `mobile-actions-008693`
  - Command: Can you please save a new contact for me? The name is Lena Petrova, the phone number is +359 888 123 456, and the email is lena.petrova.design@webmail.com.
  - Gold: `{"name": "create_contact", "arguments": {"last_name": "Petrova", "phone_number": "+359 888 123 456", "email": "lena.petrova.design@webmail.com", "first_name": "Lena"}, "raw": {"name": "create_contact", "arguments": {"last_name": "Petrova", "phone_number": "+359 888 123 456", "email": "lena.petrova.design@webmail.com", "first_name": "Lena"}}, "parse_error": null}`
  - Prediction: `{"name": null, "arguments": {}, "raw": "ara\",\"arguments\":{\"treate_calendar_tings\",\"arguments\":{\"title\":\"dentist\",\"datetuments\":{\"title\":\"dentist\",\"datet", "parse_error": "Expecting ':' delimiter: line 1 column 25 (char 24)"}`

- Source: `babyA-eval.jsonl` / ID: `mobile-actions-008694`
  - Command: Please send an email to javier.ortega@ecotradeintl.com with the subject 'Update on Q4 Report' and the body 'I've uploaded the revised figures to the shared drive. Let me know if you have any questions.'
  - Gold: `{"name": "send_email", "arguments": {"to": "javier.ortega@ecotradeintl.com", "subject": "Update on Q4 Report", "body": "I've uploaded the revised figures to the shared drive. Let me know if you have any questions."}, "raw": {"name": "send_email", "arguments": {"to": "javier.ortega@ecotradeintl.com", "subject": "Update on Q4 Report", "body": "I've uploaded the revised figures to the shared drive. Let me know if you have any questions."}}, "parse_error": null}`
  - Prediction: `{"name": null, "arguments": {}, "raw": "\"-tings\",\"arguments\":{\"title\":\"create_calendar_mdate\",\"datetuments\":{\"title\":\"dentist\",\"datetime\":\"2020-", "parse_error": "Unterminated string starting at: line 1 column 78 (char 77)"}`

- Source: `babyA-eval.jsonl` / ID: `mobile-actions-008695`
  - Command: I need to save a new contact. The full name is Anya Sharma, the phone number is +91 98765 43210, and the email address is anya.sharma@examplemail.co.in.
  - Gold: `{"name": "create_contact", "arguments": {"last_name": "Sharma", "phone_number": "+91 98765 43210", "email": "anya.sharma@examplemail.co.in", "first_name": "Anya"}, "raw": {"name": "create_contact", "arguments": {"last_name": "Sharma", "phone_number": "+91 98765 43210", "email": "anya.sharma@examplemail.co.in", "first_name": "Anya"}}, "parse_error": null}`
  - Prediction: `{"name": null, "arguments": {}, "raw": "\",\"arguments\":{\"tle\":\"dentistame\":\"sitle\",\"phone_name\":\"title\":\"dentist\",\"datetuments\":{\"title\":\"dentist\",\"", "parse_error": "Expecting ',' delimiter: line 1 column 20 (char 19)"}`

- Source: `babyA-eval.jsonl` / ID: `mobile-actions-008696`
  - Command: Please set up a new calendar event for 'Team Lunch with Marketing' on May 13, 2025 at 1:30 PM.
  - Gold: `{"name": "create_calendar_event", "arguments": {"title": "Team Lunch with Marketing", "datetime": "2025-05-13T13:30:00"}, "raw": {"name": "create_calendar_event", "arguments": {"title": "Team Lunch with Marketing", "datetime": "2025-05-13T13:30:00"}}, "parse_error": null}`
  - Prediction: `{"name": null, "arguments": {}, "raw": "flash.{\"name\":\"show_map\",\"arguments\":{\"title\":\"dentist\",\"arguments\":{\"title\":\"dentist\",\"datetuments\":{\"title", "parse_error": "Unterminated string starting at: line 1 column 97 (char 96)"}`

- Source: `babyA-eval.jsonl` / ID: `mobile-actions-008697`
  - Command: Please send an email to Kenji Tanaka at kenji.tanaka@corpmail.jp. The subject should be 'Revised Q3 Budget Figures' and the message body should be 'Please review the updated budget sheet for Q3. I had to adjust the travel expenses based on the new vendor quotes.'
  - Gold: `{"name": "send_email", "arguments": {"to": "kenji.tanaka@corpmail.jp", "subject": "Revised Q3 Budget Figures", "body": "Please review the updated budget sheet for Q3. I had to adjust the travel expenses based on the new vendor quotes."}, "raw": {"name": "send_email", "arguments": {"to": "kenji.tanaka@corpmail.jp", "subject": "Revised Q3 Budget Figures", "body": "Please review the updated budget sheet for Q3. I had to adjust the travel expenses based on the new vendor quotes."}}, "parse_error": null}`
  - Prediction: `{"name": null, "arguments": {}, "raw": "\",\"arguments\":{\"title\":\"dentist\",\"arguments\":{\"title\":\"dentist\",\"datetime\":\"2020-12-11t10:", "parse_error": "Unterminated string starting at: line 1 column 62 (char 61)"}`

## Wrong Tool

- Source: `babyA-eval.jsonl` / ID: `mobile-actions-008871`
  - Command: Please add a new contact for Kenji Tanaka. His phone number is 090-1234-5678 and his email address is k.tanaka@example.jp.
  - Gold: `{"name": "create_contact", "arguments": {"last_name": "Tanaka", "phone_number": "090-1234-5678", "email": "k.tanaka@example.jp", "first_name": "Kenji"}, "raw": {"name": "create_contact", "arguments": {"last_name": "Tanaka", "phone_number": "090-1234-5678", "email": "k.tanaka@example.jp", "first_name": "Kenji"}}, "parse_error": null}`
  - Prediction: `{"name": "show_map", "arguments": {"quarguments": "title", "phone_name": "title"}, "raw": "{\"name\":\"show_map\",\"arguments\":{\"quarguments\":\"title\",\"phone_name\":\"title\"}}}", "parse_error": null}`

- Source: `babyA-eval.jsonl` / ID: `mobile-actions-008888`
  - Command: Please create a new calendar event named "Quarterly Budget Review" for Monday, April 7th, 2025, at 2:00 PM.
  - Gold: `{"name": "create_calendar_event", "arguments": {"title": "Quarterly Budget Review", "datetime": "2025-04-07T14:00:00"}, "raw": {"name": "create_calendar_event", "arguments": {"title": "Quarterly Budget Review", "datetime": "2025-04-07T14:00:00"}}, "parse_error": null}`
  - Prediction: `{"name": "show_mam", "arguments": {"quarguments": "title", "phone_name": "title"}, "raw": "\":{\"name\":\"show_mam\",\"arguments\":{\"quarguments\":\"title\",\"phone_name\":\"title\"}}}", "parse_error": null}`

- Source: `babyA-eval.jsonl` / ID: `mobile-actions-009024`
  - Command: Send an email to Sofia Rodriguez at sofia.rodriguez@examplecorp.net. The subject should be 'Quarterly Project Update Meeting' and the body should be 'Hi Sofia, Can we schedule a quick call next week to go over the project updates? Please let me know what time works best for you. Thanks!'.
  - Gold: `{"name": "send_email", "arguments": {"to": "sofia.rodriguez@examplecorp.net", "subject": "Quarterly Project Update Meeting", "body": "Hi Sofia, Can we schedule a quick call next week to go over the project updates? Please let me know what time works best for you. Thanks!"}, "raw": {"name": "send_email", "arguments": {"to": "sofia.rodriguez@examplecorp.net", "subject": "Quarterly Project Update Meeting", "body": "Hi Sofia, Can we schedule a quick call next week to go over the project updates? Please let me know what time works best for you. Thanks!"}}, "parse_error": null}`
  - Prediction: `{"name": "treate_calendar_event", "arguments": {"title": "dentist", "datetime": "2020-12-11t11:{"}, "raw": ".{\"name\":\"treate_calendar_event\",\"arguments\":{\"title\":\"dentist\",\"datetime\":\"2020-12-11t11:{\"}}", "parse_error": null}`

- Source: `babyA-eval.jsonl` / ID: `mobile-actions-009025`
  - Command: Please schedule a calendar event titled "Dentist Check-up with Dr. Anya Sharma" for Tuesday, November 12, 2024, at 10:30 AM.
  - Gold: `{"name": "create_calendar_event", "arguments": {"title": "Dentist Check-up with Dr. Anya Sharma", "datetime": "2024-11-12T10:30:00"}, "raw": {"name": "create_calendar_event", "arguments": {"title": "Dentist Check-up with Dr. Anya Sharma", "datetime": "2024-11-12T10:30:00"}}, "parse_error": null}`
  - Prediction: `{"name": "show_map", "arguments": {"title": "dentist", "phone_name": "title"}, "raw": "flash.{\"name\":\"show_map\",\"arguments\":{\"title\":\"dentist\",\"phone_name\":\"title\"}}}", "parse_error": null}`

- Source: `babyA-eval.jsonl` / ID: `mobile-actions-009030`
  - Command: Please turn off my flashlight and also send an email to juan.perez@constructoraatlas.mx with the subject 'Project Milestones Update' and the message body 'The foundation work is 80% complete and we are on schedule for the November 1st deadline.'
  - Gold: `{"name": "turn_off_flashlight", "arguments": {}, "raw": {"name": "turn_off_flashlight", "arguments": {}}, "parse_error": null}`
  - Prediction: `{"name": "show_map", "arguments": {"quarguments": "title", "phone_name": "title"}, "raw": "{\"name\":\"show_map\",\"arguments\":{\"quarguments\":\"title\",\"phone_name\":\"title\"}}}", "parse_error": null}`

## Wrong Arguments

- Source: `babyA-eval.jsonl` / ID: `mobile-actions-008867`
  - Command: Can you show me the location of the Avenida Central Hostel in San José, Costa Rica on a map?
  - Gold: `{"name": "show_map", "arguments": {"query": "Avenida Central Hostel in San José, Costa Rica"}, "raw": {"name": "show_map", "arguments": {"query": "Avenida Central Hostel in San José, Costa Rica"}}, "parse_error": null}`
  - Prediction: `{"name": "show_map", "arguments": {"quarguments": "title", "phone_name": "title"}, "raw": "{\"name\":\"show_map\",\"arguments\":{\"quarguments\":\"title\",\"phone_name\":\"title\"}}}", "parse_error": null}`

- Source: `babyA-eval.jsonl` / ID: `mobile-actions-009295`
  - Command: Please show me the location of Livraria Lello in Porto on a map.
  - Gold: `{"name": "show_map", "arguments": {"query": "Livraria Lello in Porto"}, "raw": {"name": "show_map", "arguments": {"query": "Livraria Lello in Porto"}}, "parse_error": null}`
  - Prediction: `{"name": "show_map", "arguments": {"quarguments": "title", "phone_name": "title"}, "raw": "{\"name\":\"show_map\",\"arguments\":{\"quarguments\":\"title\",\"phone_name\":\"title\"}}}", "parse_error": null}`

- Source: `babyA-eval.jsonl` / ID: `mobile-actions-009632`
  - Command: Can you show me the location of Le Petit Cafe at 14 Rue des Fleurs, Paris, on the map?
  - Gold: `{"name": "show_map", "arguments": {"query": "Le Petit Cafe at 14 Rue des Fleurs, Paris"}, "raw": {"name": "show_map", "arguments": {"query": "Le Petit Cafe at 14 Rue des Fleurs, Paris"}}, "parse_error": null}`
  - Prediction: `{"name": "show_map", "arguments": {"title": "dentist", "phone_name": "title"}, "raw": "flash.{\"name\":\"show_map\",\"arguments\":{\"title\":\"dentist\",\"phone_name\":\"title\"}}}", "parse_error": null}`

- Source: `babyB-eval.jsonl` / ID: `mobile-actions-008721`
  - Command: I need to locate the nearest branch of 'The Corner Bakery' cafe at 3850 N Sheridan Rd on the map right now.
  - Gold: `{"name": "show_map", "arguments": {"query": "The Corner Bakery at 3850 N Sheridan Rd"}, "raw": {"name": "show_map", "arguments": {"query": "The Corner Bakery at 3850 N Sheridan Rd"}}, "parse_error": null}`
  - Prediction: `{"name": "show_map", "arguments": {"query": "mail-020-101-10t10:00:00"}, "raw": "{\"name\":\"show_map\",\"arguments\":{\"query\":\"mail-020-101-10t10:00:00\"}}", "parse_error": null}`

- Source: `babyB-eval.jsonl` / ID: `mobile-actions-008737`
  - Command: Can you show me the location of the Rijksmuseum in Amsterdam on the map?
  - Gold: `{"name": "show_map", "arguments": {"query": "Rijksmuseum in Amsterdam"}, "raw": {"name": "show_map", "arguments": {"query": "Rijksmuseum in Amsterdam"}}, "parse_error": null}`
  - Prediction: `{"name": "show_map", "arguments": {"query": "mail-020-101-10t10:00:00"}, "raw": "{\"name\":\"show_map\",\"arguments\":{\"query\":\"mail-020-101-10t10:00:00\"}}", "parse_error": null}`
