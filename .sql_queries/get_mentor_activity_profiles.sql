SELECT u.id, p.username, p.email AS profile_email, u.email AS facebook_email, s.messages_sent, r.messages_received, u.last_login
FROM auth_user AS u
LEFT JOIN profiles_gamecoachprofile AS p
ON p.user_id = u.id
LEFT JOIN (
	SELECT sender_id, COUNT(sender_id) AS messages_sent
	FROM postman_message
	GROUP BY sender_id
) AS s
ON s.sender_id = u.id
LEFT JOIN (
	SELECT recipient_id, COUNT(recipient_id) AS messages_received
	FROM postman_message
	GROUP BY recipient_id
) AS r
ON r.recipient_id = u.id
WHERE is_mentor = True
GROUP BY u.id, p.username, p.email, u.email, s.messages_sent, r.messages_received, u.last_login