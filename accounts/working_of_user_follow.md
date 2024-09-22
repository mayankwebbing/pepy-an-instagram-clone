```bash
>>> from accounts.models import Profile
>>> 
>>> mayankadmin = Profile.objects.get(username="mayankadmin")
>>> doyen = Profile.objects.get(username="doyen")
>>> 
>>> narendramodi = Profile.objects.get(username="narendramodi")
>>> ranveersingh = Profile.objects.get(username="ranveersingh")
>>> kapilsharma = Profile.objects.get(username="kapilsharma")
>>> iamsrk = Profile.objects.get(username="iamsrk")
>>> hrithikroshan = Profile.objects.get(username="hrithikroshan")
>>> 
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

>>> Post.objects.filter(user_id__in = doyen.following.all()).order_by('-created_at') 
<QuerySet [<Post: @mayankadmin posted on 2024-07-05 17:08:46.620366+00:00>, <Post: @narendramodi posted on 2024-07-04 08:03:27.415860+00:00>, <Post: @narendramodi posted on 2024-07-04 08:02:48.596340+00:00>, <Post: @mayankadmin posted on 2024-07-03 08:27:50.653950+00:00>, 
<Post: @mayankadmin posted on 2024-07-03 07:48:04.164513+00:00>, <Post: @mayankadmin posted on 2024-07-03 07:43:21.081297+00:00>, <Post: @mayankadmin posted on 2024-07-03 07:32:10.164032+00:00>]>

>>> print(Post.objects.filter(user_id__in = doyen.following.all()).order_by('-created_at').query)
SELECT "feed_post"."id", "feed_post"."user_id_id", "feed_post"."caption", "feed_post"."created_at", "feed_post"."updated_at" FROM "feed_post" WHERE "feed_post"."user_id_id" IN (SELECT U0."id" FROM "accounts_profile" U0 INNER JOIN "accounts_profile_followers" U1 ON (U0."id" = U1."from_profile_id") WHERE U1."to_profile_id" = ccf240c3-970b-42ed-9cb4-eb007e1fe89c) ORDER BY "feed_post"."created_at" DESC
>>>