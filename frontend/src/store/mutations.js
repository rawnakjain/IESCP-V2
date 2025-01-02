export default {
    // there is nothing here
    setAuth(state, payload) {
        state.isLoggedIn = true;
        state.username = payload.username;
        state.token = payload.token;
        state.role = payload.role;
        state.active = payload.active;
        state.expiresIn = payload["expires_in"];
    },
    setError(state, error) {
        state.error = error;
    },
    setSuccess(state, success) {
        state.success = success;
    },
    setLogIn(state, payload) {
        state.isLoggedIn = payload
    },
    setInfluencers(state, influencers) { // Sponsor Influencers List
        state.influencers = influencers;
    },
    setSponsors(state, sponsors) { // Admin Sponsors List
        state.sponsors = sponsors;
    },
    setSponsorCampaigns(state, campaigns) { // Sponsor Campaigns List
        state.sponsorCampaigns = campaigns;
    },
    setCampaignStatus(state, status) { // Sponsor Create Campaign Status
        state.campaignStatus = status;
    },
    setCampaign(state, campaign) { // Fetching a specific campaign to update the details
        state.campaign = campaign;
    },
    removeCampaign(state, campaignId) { // Remove a campaign from the list
        state.sponsorCampaigns = state.sponsorCampaigns.filter(campaign => campaign.id !== campaignId);
    },
    setCampaignAds(state, ads) { // Fetching ads for a specific campaign
        state.campaignAds = ads;
    },
    setAd(state, ad) { // Fetching a specific ad for updating purpose
        state.ad = ad;
    },
    removeAd(state, adId) { // Remove an ad from the list
        state.campaignAds = state.campaignAds.filter(ad => ad.id !== adId);
    },
    updateAd(state, updatedAd) {
        const index = state.campaignAds.findIndex(ad => ad.id === updatedAd.id);
        if (index !== -1) {
            state.campaignAds.splice(index, 1, updatedAd);
        }
    },
    setAdStatus(state, status) { // Create Ad Status
        state.adStatus = status;
    },


    // Influencer Actions
    setAllCampaigns(state, campaigns) { // Influencer All Campaigns List
        state.allCampaigns = campaigns;
    },
    setInfluencerAds(state, ads) { // Influencer Ads List
        state.influencerAds = ads;
    },
    setInfluencerCampaigns(state, campaigns) { // Influencer Campaigns List
        state.influencerCampaigns = campaigns;
    },
    setCeleryWaiting(state, waiting) {
        state.waiting = waiting;
    },
    setSearchResults(state, results) {
        state.searchResult = results;
    },

    // Admin's Chart
    setUserbaseData(state, data){
      state.UserbaseData = data;
    },
    setCampaignData(state, data){
        state.campaignData = data;
    },
    setAdsData(state, data){
        state.adsData = data;
    }

}