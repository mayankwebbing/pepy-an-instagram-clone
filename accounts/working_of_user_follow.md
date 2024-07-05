```bash
>>> from accounts.models import Profile
>>> 
>>> mayankadmin = Profile.objects.get(username="mayankadmin")
>>> 
>>> narendramodi = Profile.objects.get(username="narendramodi")
>>> ranveersingh = Profile.objects.get(username="ranveersingh")
>>> kapilsharma = Profile.objects.get(username="kapilsharma")
>>> iamsrk = Profile.objects.get(username="iamsrk")
>>> hrithikroshan = Profile.objects.get(username="hrithikroshan")
>>> 
>>> doyen = Profile.objects.get(username="doyen")
>>> rashmika_mandanna = Profile.objects.get(username="rashmika_mandanna")
>>> nehakakkar = Profile.objects.get(username="nehakakkar")
>>> 
>>> mayankadmin.following.add(narendramodi)
>>> mayankadmin.following.add(ranveersingh)
>>> mayankadmin.following.add(kapilsharma)
>>> mayankadmin.following.add(iamsrk)
>>> mayankadmin.following.add(hrithikroshan)
>>> 
>>> doyen.following.add(mayankadmin)
>>> rashmika_mandanna.following.add(mayankadmin)
>>> 
>>> Profile.objects.filter(following=mayankadmin) 
<QuerySet [<Profile: @doyen Profile>, <Profile: @rashmika_mandanna Profile>]>
>>> 
>>> mayankadmin.following.all()                   
<QuerySet [<Profile: @narendramodi Profile>, <Profile: @ranveersingh Profile>, <Profile: @kapilsharma Profile>, <Profile: @iamsrk Profile>, <Profile: @hrithikroshan Profile>]>
>>> 
>>> mayankadmin.following.add(nehakakkar)
>>>  
>>> mayankadmin.following.all()
<QuerySet [<Profile: @narendramodi Profile>, <Profile: @ranveersingh Profile>, <Profile: @kapilsharma Profile>, <Profile: @iamsrk Profile>, <Profile: @hrithikroshan Profile>, <Profile: @nehakakkar Profile>]>
```