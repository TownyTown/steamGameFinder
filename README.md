# steamGameFinder

👋 Hi, all this does is try to find bugged games that add +1 to game badge counter on Steam.

    Note; This takes a long time to run since it needs to check about ~550,000 appID's for validiity




## Basic stuff
Requires Python 3.12+ to run and 'httpx' library.

Run main.py and it'll start scraping for bugged games, search or filter the searched.txt file for "9999" to find them.

Automatically saves/resumes progress of last checked appID so no need to worry about stopping it.


### TODO Tasks 
- [ ] Upload a fully checked appID list for faster rechecking
- [ ] Add multi-threading / batch processing since ASync is doneish that doesn't break the save order >:(
- [ ] Add functionality to recheck known appID's
- [ ] Create verification script to automatically check if the game actually adds a +1 to counter

### Completed Tasks ✓
- [x] Add saving/resuming progress from last appID checked
- [x] Convert to ASync
