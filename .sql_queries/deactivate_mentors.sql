UPDATE auth_user SET is_active = FALSE
WHERE id IN
(
	SELECT  user_id
	FROM profiles_gamecoachprofile WHERE username IN 
		(
			# Usernames
		)
);