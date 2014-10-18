SELECT a.username AS from_internal, p.username AS from_username, p.is_mentor AS from_ismentor, a.email AS from_email_internal, p.email  AS from_email_profile, b.username AS to_interal, p2.username AS to_username, p2.is_mentor AS to_ismentor, b.email AS to_email_internal, p2.email AS to_email_profile, body, sent_at,  to_char(current_timestamp, 'YYYY-MM-DD HH12:MI:SS') AS sent_at_date
FROM postman_message AS m
LEFT JOIN auth_user AS a
ON m.sender_id = a.id
LEFT JOIN auth_user AS b
ON m.recipient_id = b.id
LEFT JOIN profiles_gamecoachprofile AS p
ON m.sender_id = p.user_id
LEFT JOIN profiles_gamecoachprofile AS p2
ON m.recipient_id = p2.user_id
ORDER BY sent_at DESC