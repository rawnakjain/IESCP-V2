import { createRouter, createWebHistory } from "vue-router";

import GetStarted from "@/components/views/GetStarted.vue";
import RegisterSponsor from "@/components/views/RegisterSponsor.vue";
import RegisterInfluencer from "@/components/views/RegisterInfluencer.vue";
import LogIn from "@/components/views/LogIn.vue";
import SponsorDashboard from "@/components/views/sponsor/SponsorDashboard.vue";
import InfluencerDashboard from "@/components/views/influencer/InfluencerDashboard.vue";
import AdminDashboard from "@/components/views/admin/AdminDashboard.vue";
import SponsorCampaigns from "@/components/views/sponsor/SponsorCampaigns.vue";
import CreateCampaign from "@/components/views/sponsor/CreateCampaign.vue";
import ProfilePage from "@/components/views/ProfilePage.vue";
import LogOut from "@/components/views/LogOut.vue";
import InfluencersList from "@/components/views/sponsor/InfluencersList.vue";
import MyCampaigns from "@/components/views/influencer/MyCampaigns.vue";
import AdRequests from "@/components/views/influencer/AdRequests.vue";
import UpdateCampaign from "@/components/views/sponsor/UpdateCampaign.vue";
import ViewCampaign from "@/components/views/sponsor/ViewCampaign.vue";
import ActiveCampaigns from "@/components/views/influencer/ActiveCampaigns.vue";
import CreateAd from "@/components/views/sponsor/CreateAd.vue";
import AdRequestList from "@/components/views/sponsor/AdRequestList.vue";
import UpdateAd from "@/components/views/sponsor/UpdateAd.vue";
import AllCampaigns from "@/components/views/admin/AllCampaigns.vue";
import AllInfluencers from "@/components/views/admin/AllInfluencers.vue";
import AllSponsors from "@/components/views/admin/AllSponsors.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', component: GetStarted },
        { path: '/register', component: GetStarted },
        { path: '/register/sponsor', component: RegisterSponsor },
        { path: '/register/influencer', component: RegisterInfluencer },
        { path: '/login', component: LogIn },
        { path: '/profile', component: ProfilePage },
        { path: '/logout', component: LogOut },

        // Sponsor routes
        { path: '/sponsor', component: SponsorDashboard },
        { path: '/sponsor/influencers-list', component: InfluencersList },
        { path: '/sponsor/campaigns', component: SponsorCampaigns },
        { path: '/sponsor/campaigns/create', component: CreateCampaign},
        { path: '/sponsor/campaigns/update/:id', component: UpdateCampaign},
        { path: '/sponsor/ads-list/:id', component: AdRequestList},
        { path: '/sponsor/campaigns/view/:id', component: ViewCampaign},
        { path: '/sponsor/ads/create', component: CreateAd},
        { path: '/sponsor/ads/update/:id', component:UpdateAd},

        // Influencer routes
        { path: '/influencer', component: InfluencerDashboard },
        { path: '/influencer/campaigns', component: ActiveCampaigns },
        { path: '/influencer/my-campaigns', component: MyCampaigns },
        { path: '/influencer/ad-requests', component: AdRequests },
        { path: '/influencer/ads/create', component: CreateAd},

        { path: '/admin', component: AdminDashboard },
        { path: '/admin/sponsors', component:AllSponsors},
        { path: '/admin/influencers', component:AllInfluencers},
        { path: '/admin/campaigns', component: AllCampaigns },
    ]
});

router.beforeEach(function(to, from, next) {
    const role = JSON.parse(localStorage.getItem('role'));

    if (to.path.startsWith('/sponsor') && role !== 'sponsor') {
        next('/login');
    } else if (to.path.startsWith('/influencer') && role !== 'influencer') {
        next('/login');
    } else if (to.path.startsWith('/admin') && role !== 'admin') {
        next('/login');
    } else {
        next();
    }
});

export default router;