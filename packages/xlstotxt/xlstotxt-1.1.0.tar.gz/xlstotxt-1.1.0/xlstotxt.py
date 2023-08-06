

'''=============================================
模块名： xlstotxt
功能：将一个xls文件数据读出，写入一个txt文件中；
========================================'''

import xlwings as xw

def xlstotxt(xls_filename,txt_filename):

	''' 两个参数：xls_filename(.xlsx 和 .xls都可以)文件全面，txt_filename为 txt文件全名，含扩展名'''

	app=xw.App(visible=False,add_book=False)
	with open(txt_filename,'w') as f:
		try:
			wb=app.books.open(xls_filename)
		except Exception as e:
			print("打开文件失败！，文件不存在，或文件为只读，已经打开的状态！")
		finally:			
		
			for sht in wb.sheets:
				nrows = sht.api.UsedRange.Rows.count
				ncols = sht.api.UsedRange.Columns.count
				old_nrows = nrows
				#print(nrows)
				#print(ncols)
				f.write(sht.name+'：=======================\n')
				#print(sht.range(nrows,ncols))
				for Rows_i in range(1,nrows+1):
					for Columns_j in range(1,ncols+1):
						try:
							var = sht.range(Rows_i,Columns_j).value
							#print(var)
							f.write(str(var) + '\t')
						except Exception as e:
							#print('读取单元格数据失败，数据应该为空！')
							f.write('\t')
						finally:
							pass
					f.write('\n')
	
	wb.close()
	app.quit()
	#print('完成！')




