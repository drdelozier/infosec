#!/usr/bin/env python
# coding: utf-8

# ### Clearance Model based on Bell-LaPadula, Chapter 5

# In[ ]:


documents = [
    { 
        'content': "alpha",
        'clearance': ('usa','confidential')
    },
    { 
        'content': "beta",
        'clearance': ('ohio','secret')
    },
    { 
        'content': "gamma",
        'clearance': ('usa','topsecret')
    },
    { 
        'content': "treats",
        'clearance': ('ohio','unclassified')
    },    
]
documents


# In[ ]:


subjects = [
    { 
        'name': "santa",
        'clearance': ('world','topsecret')
    },
    { 
        'name': "dorothy",
        'clearance': ('ohio','confidential')
    },
    { 
        'name': "roger",
        'clearance': ('usa','secret')
    }
]
subjects


# In[ ]:


def level_dominates(a, b):
    # print("does level",a,"dominate",b,"?")
    levels = ['unclassified', 'confidential', 'secret', 'topsecret']
    if (a in levels) and (b in levels):
        return levels.index(a) >= levels.index(b)
    return False

pairs = [
    ('unclassified','secret'),
    ('secret','unclassified'),
    ('secret','secret'),   
    ('topsecret','confidential')    
]
          
for pair in pairs:
    a, b = pair
    print(a, b, level_dominates(a,b))


# In[ ]:


regions = {
    'world' : ['usa','europe'],
    'usa' : ['delaware','ohio','kansas'],
    'europe' : ['france','germany','spain'],
    'ohio' : ['cuyahoga','summit','portage','medina'],
    'delaware' : ['wilmington','dover'],
    'germany' : ['munich','berlin','hanover'],
    'summit' : ['akron','fairlawn'],
    'akron' : ['highland_square','uakron']
}

def region_dominates(a, b):
    # print("does region",a,"dominate",b,"?")
    if (a == b):
        return True
    if not a in regions:
        return False
    if b in regions[a]:
        return True
    for region in regions[a]:
        if region_dominates(region,b):
            return True
    return False
    
pairs = [
    ('usa','ohio'),
    ('europe','europe'),
    ('africa','ohio'),
    ('usa','france'),
    ('ohio','portage'),
    ('usa','portage'),
    ('usa','akron'),
    ('usa','highland_square'),
    ('europe','portage'),
    ('ohio','usa')
]
          
for pair in pairs:
    a, b = pair
    print(a, b, region_dominates(a,b))    


# In[ ]:





# In[ ]:


def dominates(a,b):
    # print("does clearance",a,"dominate",b,"?")
    region_a, level_a = a
    region_b, level_b = b
    if level_b == "unclassified":
        return True
    return region_dominates(region_a, region_b) and level_dominates(level_a, level_b)

print(dominates(('usa','secret'),('ohio','confidential')))
print(dominates(('usa','confidential'),('ohio','secret')))
print(dominates(('usa','secret'),('ohio','secret')))
print(dominates(('usa','secret'),('europe','secret')))
print(dominates(('world','secret'),('uakron','secret')))


# In[ ]:


def simple_security(subject, document):
    return dominates(subject['clearance'],document['clearance'])

def star_property(subject, document):
    return dominates(document['clearance'],subject['clearance'])

def can_read(subject, document):
    return simple_security(subject, document)

def can_write(subject, document):
    return star_property(subject, document)


# In[ ]:


can_read(subjects[0],documents[1])


# In[ ]:


can_read(subjects[2],documents[2])


# In[ ]:


for subject in subjects:
    for document in documents:
        if can_read(subject, document):
            print(subject['name'],'can read',document['content'])
        else:
            print(subject['name'],'can not read',document['content'])


# In[ ]:


for subject in subjects:
    for document in documents:
        if can_write(subject, document):
            print(subject['name'],'can write',document['content'])
        else:
            print(subject['name'],'can not write',document['content'])


# In[ ]:




