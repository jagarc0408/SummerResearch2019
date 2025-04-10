#Works for labeled_whichever_.csv NOT FOR image_labels.csv or sessions.csv
import csv
import re

insta = []
with open("labeled_0plus_to_10__full.csv", encoding='latin-1') as fd:
    rd = csv.reader(fd, delimiter=",", quotechar='"')
    for row in rd:
        insta.append(row)

#Building Lists to hold data

unit_ids = []       #Unit ID
bullying = []       #Annotator bullying decision
aggression = []     #Annotator aggression decision
caption_time = []   #Caption Time for original post
image_urls = []     #Image URL for original post
likes = []          #Number of Likes on original post
owner_comments = [] #Original post owner's caption
owner_id = []       #Username for original poster
for row in insta:
    unit_ids.append(row[0])
    aggression.append(row[14])
    bullying.append(row[15])
    caption_time.append(row[211])
    image_urls.append(row[212])
    likes.append(row[213])
    owner_comments.append(row[214])
    owner_id.append(row[215])

#Gets all comments/replies to original post

all_comments_list = []
for row in insta:
    count = 15
    comment_row = []
    while count < 210:
        count = count + 1
        comment_row.append(row[count])
    all_comments_list.append(comment_row)
    
#Cleans html tags from replies

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    #cleantext = cleantext.replace('created_at:', '')
    if cleantext != 'empety':
        x = cleantext.split(' ', 1)[0] #This is where usernames are
        y = re.findall("\(created_at:.*\)", cleantext)
        #print(y)
        return cleantext
         
all_comments_clean = []

for i in range(0, len(all_comments_list)):
    temp_clean_row = []
    for j in range(0, len(all_comments_list[i])):
       temp_clean_row.append(cleanhtml(all_comments_list[i][j])) 
    all_comments_clean.append(temp_clean_row)
    
    

#Gets Times for each reply)
#print(re.split(" ",all_comments_clean[1][0],1))  

aggression_binary = [] #This is majority list
lc = 0
y = 0
for i in range(1, len(aggression)):
    if aggression[i][0].lower() == 'a':
        y += 1
        lc = lc + 1
    else:
        lc = lc + 1
        
    if lc == 5 and y >= 3:
        aggression_binary.append(1)
        lc = 0
        y = 0
    elif lc ==5 and y < 3:
        aggression_binary.append(0)
        lc = 0
        y = 0
        
bullying_binary = [] #This is majority list
lc = 0
y = 0
for i in range(1, len(aggression)):
    if bullying[i][0].lower() == 'b':
        y += 1
        lc = lc + 1
    else:
        lc = lc + 1
        
    if lc == 5 and y >= 3:
        bullying_binary.append(1)
        lc = 0
        y = 0
    elif lc ==5 and y < 3:
        bullying_binary.append(0)
        lc = 0
        y = 0

ui = []
for i in range(1, len(unit_ids)):
    if unit_ids[i-1] != unit_ids[i]:
        ui.append(unit_ids[i])

with open('instaInfo.tsv', 'wt', encoding="utf-8",newline='') as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t', lineterminator='\n')
    tsv_writer.writerow(['UnitID', 'Aggression Majority', 'Bullying Majority', 'Timestamp'])
    for i in range(len(aggression_binary)):
        tsv_writer.writerow([ui[i], aggression_binary[i], bullying_binary[i]])
        
            
    
