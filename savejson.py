def JsonWrite(fn, data):
    #json 파일로 저장
    with open(fn, 'w', encoding='UTF-8-sig') as make_file:
        json.dump(data, 
        	make_file, 
        	indent="\t", 
        	cls=NpEncoder, 
        	ensure_ascii=False)

# 날짜 지정(파일명 설정을 위해)
now = datetime.datetime.now()
nowDate = now.strftime('%Y_%m_%d')
nds = str(nowDate)

# 파일명(위치까지) 설정 - *절대경로 주의*
fn1 = '/home/ec2-user/app/diq/data/' + str(nds) + '/dailyUpdateData.json'

# 디렉토리 생성 - *절대경로 주의*
dn = '/home/ec2-user/app/diq/data/' + str(nds)
if os.path.isdir(dn):
    shutil.rmtree(dn)
os.mkdir(dn)

#json 파일로 저장
JsonWrite(fn1, result)
