import re
 
MINIMUM_PASSWORD_LENGTH = 6
REGEX_VALID_PASSWORD = (
	## Don't allow any spaces, e.g. '\t', '\n' or whitespace etc.
	r'^(?!.*[\s])'
	## Minimum 6 characters
	'{' + str(MINIMUM_PASSWORD_LENGTH) + ',}$')
 
 
def validate_password(password):
	if re.match(REGEX_VALID_PASSWORD, password):
		return True
	return False