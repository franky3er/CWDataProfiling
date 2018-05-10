SOURCE_CSV_FILE_PATH = 'Daten/FD_Incidents_2016_2017_Archiviert_EOC_EOR_separated.csv'
TARGET_CSV_FILE_PATH = 'Daten/FD_Incidents_2016_2017_Archiviert_for_Python.csv'
SOURCE_ROW_DELIMITER = '<EOR>'
SOURCE_COL_DELIMITER = '<EOC>'
TARGET_ROW_DELIMITER = '\n'
TARGET_COL_DELIMITER = ';'
QUOTATION_DELIMITER = '""'

def delimited(file, delimiter='\n'):
	file_content = file.read()
	return (row for row in file_content.split(delimiter))
		
def convert_to_valid_csv_column(
		source_column, 	
		target_row_delimiter,
		target_col_delimiter, 
		quotation_delimiter
	):
	target_column = source_column
	if source_column == None or source_column == '':
		return target_column
	if (
			target_row_delimiter in source_column 
			or target_col_delimiter in source_column
			or ('"' == source_column[0] and '"' == source_column[-1])
		):
		target_column = '"' + target_column.replace('"', QUOTATION_DELIMITER) + '"'
	return target_column
		
def convert_to_valid_csv_row(
		source_row, 
		source_col_delimiter,
		target_row_delimiter,
		target_col_delimiter,
		quotation_delimiter
	):
	if source_row == None or source_row == '': 
		return None
	target_row = ''
	source_columns = source_row.split(source_col_delimiter)
	for source_column in source_columns:
		target_column = convert_to_valid_csv_column(
			source_column, 
			target_row_delimiter, 
			target_col_delimiter, 
			quotation_delimiter
		) 
		target_row += (target_col_delimiter if target_row != '' else '') + target_column
	return target_row + target_row_delimiter
		
def convert_to_valid_csv(
		source_csv_file_path, 
		target_csv_file_path, 
		source_row_delimiter, 
		source_col_delimiter, 
		target_row_delimiter,
		target_col_delimiter,
		quotation_delimiter
	):
	source_csv_file = open(source_csv_file_path, encoding='utf16')
	target_csv_file = open(target_csv_file_path, "w", encoding='utf16')
	source_rows = delimited(source_csv_file, source_row_delimiter)
	row_idx = 0
	for source_row in source_rows:
		row_idx+=1
		print ("Processing Row: " + str(row_idx))
		target_row = convert_to_valid_csv_row(
			source_row, 
			source_col_delimiter, 
			target_row_delimiter,
			target_col_delimiter,
			quotation_delimiter
		)
		if target_row:
			target_csv_file.write(target_row)
	target_csv_file.close()
	source_csv_file.close()
		
convert_to_valid_csv(
	SOURCE_CSV_FILE_PATH, 
	TARGET_CSV_FILE_PATH, 
	SOURCE_ROW_DELIMITER, 
	SOURCE_COL_DELIMITER, 
	TARGET_ROW_DELIMITER,
	TARGET_COL_DELIMITER,
	QUOTATION_DELIMITER
)

