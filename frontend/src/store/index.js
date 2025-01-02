import {createStore} from "vuex";
import mutations from "@/store/mutations";
import getters from "@/store/getters";
import actions from "@/store/actions";


const store = createStore({
    state() {
        return {
            isLoggedIn: false,
            username: "",
            token: "",
            role: "",
            active: "",
            error: "",
            success: false,
            expiresIn: null,

            // Sponsor Dashboard Data
            influencers: [], // list of influencers
            sponsorCampaigns: [], // list of campaigns created by the sponsor
            campaignStatus: "", // message received during campaign creation
            campaign: {}, // fetching a specific campaign to update the details
            campaignUpdateStatus: "", // message received during campaign update
            campaignAds:[], //fetching ads of a specific campaign
            ad: {}, //fetching a specific ad to update the details just like campaign{}

            adStatus: "", // message received during ad creation or changing the status of an ad

            // Influencer Dashboard Data
            allCampaigns: [], // list of all campaigns available to the influencer
            influencerAds: [], // list of ads created by the influencer
            influencerCampaigns: [], // list of campaigns joined by the influencer

            //async celery
            waiting: false,

            //search
            searchResult: [],

            //admin dash
            sponsors: [], // list of sponsors
            UserbaseData:[],
            campaignData:[],
            adsData:[],
        };
    },
    getters: getters,
    mutations: mutations,
    actions: actions,
});

export default store;