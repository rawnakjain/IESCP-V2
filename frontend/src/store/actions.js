export default {
    async submitForm(context, form) {
        try {
            const response = await fetch("http://127.0.0.1:5000/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(form),
            });
            const data = await response.json();
            if (response.status > 299 || response.status < 200) {
                context.commit("setError", data["message"]);
            } else {
                context.commit("setSuccess", true);
                context.commit("setLogIn", true)
            }
        } catch (error) {
            console.error("Error:", error);
        }
    },

    async login(context, form) {
        try {
            const response = await fetch("http://127.0.0.1:5000/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(form),
            });

            const responseText = await response.text(); // Get the response text
            // console.log("Response Text:", responseText); // Log the response text

            if (!responseText) {
                throw new Error("Empty response from server");
            }

            const data = JSON.parse(responseText); // Parse the response text as JSON

            if (!response.ok) {
                context.commit("setError", data["message"]);
                throw new Error(`HTTP error!`);
            }

            if (data.token) {
                localStorage.setItem("token", JSON.stringify(data.token));
                localStorage.setItem("username", JSON.stringify(data.username));
                localStorage.setItem("role", JSON.stringify(data.role));
                localStorage.setItem("active", JSON.stringify(data.active));
                localStorage.setItem("expires_in", JSON.stringify(data["expires_in"]));
                localStorage.setItem("user_id", JSON.stringify(data["user_id"]));
            }

            context.commit("setAuth", data);

        } catch (error) {
            console.error('Error logging in:', error);
        }
    },

    async updateUserDetails(context, form) {
        const username = form.username
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/profile/${username}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(form),
            });
            const data = await response.json();
            console.log(data)
            if (response.status > 299 || response.status < 200) {
                context.commit("setError", data["message"]);
            }
            context.commit("setSuccess", true);
            return data
        } catch (error) {
            console.error("Error:", error);
        }
    },

    async fetchProfile(context, username) {
        username = JSON.parse(username)
        try {
            const token = JSON.parse(localStorage.getItem("token"));
            const response = await fetch(`http://127.0.0.1:5000/api/profile/${username}`, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error("Error fetching profile:", error);
            context.commit("setError", error.message);
        }
    },

    async fetchInfluencers(context) {
        try {
            const token = JSON.parse(localStorage.getItem("token"));
            const response = await fetch("http://127.0.0.1:5000/api/influencers-list", {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            });
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            const data = await response.json();
            context.commit("setInfluencers", data);
        } catch (error) {
            console.error("Error fetching influencers:", error);
        }
    }, //fetching influencers list

    async fetchSponsorCampaigns(context) {
        try {
            const token = JSON.parse(localStorage.getItem("token"));
            const role = JSON.parse(localStorage.getItem("role"));

            if (role !== "sponsor") {
                throw new Error("User is not a sponsor");
            }

            const response = await fetch("http://127.0.0.1:5000/api/sponsor/campaigns-list", {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                },
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await response.json();
            context.commit("setSponsorCampaigns", data);
        } catch (error) {
            console.error("Error fetching sponsor campaigns:", error);
        }
    }, //fetching sponsor created campaigns list

    async createCampaign(context, form) {
        console.log("inside function");
        try {
            const token = JSON.parse(localStorage.getItem("token"));
            const role = JSON.parse(localStorage.getItem("role"));

            if (role !== "sponsor") {
                throw new Error("User is not a sponsor");
            }

            const response = await fetch("http://127.0.0.1:5000/api/campaign", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify(form)
            });

            const data = await response.json();

            if (!response.ok) {
                context.commit("setError", data.message);
                throw new Error(data.message);
            }
            context.commit("setCampaignStatus", data.message);
            context.commit('setSuccess', true);
        } catch (error) {
            console.error("Error creating campaign:", error);
            context.commit("setError", error.message);
        }
    }, //creating a campaign by a sponsor

    async fetchCampaign(context, campaignId) {
        try {
            const token = JSON.parse(localStorage.getItem("token"));
            const role = JSON.parse(localStorage.getItem("role"));

            if (role !== "sponsor") {
                throw new Error("User is not a sponsor");
            }

            const response = await fetch(`http://127.0.0.1:5000/api/campaign/${campaignId}`, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                },
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await response.json();
            context.commit("setCampaign", data);
            context.commit("setCampaignStatus", data.message);
            context.commit("setSuccess", true);
        } catch (error) {
            console.error("Error fetching campaign:", error);
        }
    }, // fetching a campaign created by a sponsor for updating

    async updateCampaign(context, form) {
        try {
            const token = JSON.parse(localStorage.getItem("token"));
            const role = JSON.parse(localStorage.getItem("role"));

            if (role !== "sponsor") {
                throw new Error("User is not a sponsor");
            }

            const response = await fetch(`http://127.0.0.1:5000/api/campaign/${form.id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify(form)
            });

            const data = await response.json();

            if (!response.ok) {
                context.commit("setError", data.message);
                throw new Error(data.message);
            }
            context.commit("setCampaign", data.message);
            context.commit("setSuccess", true);
        } catch (error) {
            console.error("Error updating campaign:", error);
            context.commit("setError", error.message);
        }
    },

    async deleteSponsorCampaign(context, campaignId) {
        try {
            const token = JSON.parse(localStorage.getItem("token"));
            const role = JSON.parse(localStorage.getItem("role"));

            if (role !== "sponsor") {
                throw new Error("User is not a sponsor");
            }

            const response = await fetch(`http://127.0.0.1:5000/api/campaign/${campaignId}`, {
                method: "DELETE",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            context.commit("removeCampaign", campaignId);
        } catch (error) {
            console.error("Error deleting campaign:", error);
            context.commit("setError", error.message);
        }
    },

    async createAd(context, form) {
        try {
            const token = JSON.parse(localStorage.getItem("token"));

            const response = await fetch("http://127.0.0.1:5000/api/ad", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify(form)
            });

            const data = await response.json();

            if (!response.ok) {
                context.commit("setError", data.message);
                throw new Error(data.message);
            }
            context.commit('setSuccess', true);
            console.log(data.message);
        } catch (error) {
            console.error("Error creating ad:", error);
            context.commit("setError", error.message);
        }
    }, //create ad

    async fetchCampaignAds(context, campaignId) {
        try {
            const token = JSON.parse(localStorage.getItem("token"));
            const role = JSON.parse(localStorage.getItem("role"));

            if (role !== "sponsor") {
                throw new Error("User is not a sponsor");
            }

            const response = await fetch(`http://127.0.0.1:5000/api/ads-list/${campaignId}`, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await response.json();
            context.commit("setCampaignAds", data);
        } catch (error) {
            console.error("Error fetching campaign ads:", error);
            context.commit("setError", error.message);
        }
    }, //fetching a particular campaign's ads

    async fetchAd(context, adId) {
        try {
            const token = JSON.parse(localStorage.getItem("token"));
            const role = JSON.parse(localStorage.getItem("role"));

            if (role !== "sponsor") {
                throw new Error("User is not a sponsor");
            }

            const response = await fetch(`http://127.0.0.1:5000/api/ad/${adId}`, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                },
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await response.json();
            context.commit("setAd", data);
            context.commit("setSuccess", true);
        } catch (error) {
            console.error("Error fetching ad:", error);
            context.commit("setError", error.message);
        }
    }, //read or fetch a particular ad

    async updateAd(context, ad) {
        try {
            const token = JSON.parse(localStorage.getItem("token"));
            const role = JSON.parse(localStorage.getItem("role"));

            if (role !== "sponsor") {
                throw new Error("User is not a sponsor");
            }

            const response = await fetch(`http://127.0.0.1:5000/api/ad/${ad.id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify(ad)
            });

            const data = await response.json();

            if (!response.ok) {
                context.commit("setError", data.message);
                throw new Error(data.message);
            }
            context.commit("updateAd", data);
            context.commit("setSuccess", true);
        } catch (error) {
            console.error("Error updating ad:", error);
            context.commit("setError", error.message);
        }
    }, //update an ad

    async deleteAd(context, adId) {
        try {
            const token = JSON.parse(localStorage.getItem("token"));
            const role = JSON.parse(localStorage.getItem("role"));

            if (role !== "sponsor") {
                throw new Error("User is not a sponsor");
            }

            const response = await fetch(`http://127.0.0.1:5000/api/ad/${adId}`, {
                method: "DELETE",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            context.commit("removeAd", adId);
            context.commit("setSuccess", true);
        } catch (error) {
            console.error("Error deleting ad:", error);
            context.commit("setError", error.message);
        }
    }, //delete an ad

    async approveAd(context, adId) {
        try {
            const token = JSON.parse(localStorage.getItem("token"));

            const response = await fetch(`http://127.0.0.1:5000/api/ad/update-status/${adId}`, {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({status: 'approved'})
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await response.json();
            console.log(data)
            context.commit("updateAd", data.ad);
            context.commit("setAdStatus", data.message);
            context.commit("setSuccess", true);
        } catch (error) {
            console.error("Error approving ad:", error);
            context.commit("setError", error.message);
        }
    },

    async declineAd(context, adId) {
        try {
            const token = JSON.parse(localStorage.getItem("token"));
            // const role = JSON.parse(localStorage.getItem("role"));

            const response = await fetch(`http://127.0.0.1:5000/api/ad/update-status/${adId}`, {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({status: 'declined'})
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await response.json();
            context.commit("updateAd", data.ad);
            context.commit("setAdStatus", data.message);
            context.commit("setSuccess", true);
        } catch (error) {
            console.error("Error declining ad:", error);
            context.commit("setError", error.message);
        }
    },

    async completeAd(context, adId) {
        try {
            const token = JSON.parse(localStorage.getItem("token"));
            const role = JSON.parse(localStorage.getItem("role"));

            if (role !== "sponsor") {
                throw new Error("User is not a sponsor");
            }

            const response = await fetch(`http://127.0.0.1:5000/api/ad/update-status/${adId}`, {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({status: 'completed'})
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await response.json();
            context.commit("updateAd", data.ad);
            context.commit("setAdStatus", data.message);
            context.commit("setSuccess", true);
        } catch (error) {
            console.error("Error completing ad:", error);
            context.commit("setError", error.message);
        }
    },

    async negotiateAd(context, {adId, negotiated_payment_amount}) {
        try {
            const token = JSON.parse(localStorage.getItem("token"));
            console.log(negotiated_payment_amount)

            const response = await fetch(`http://127.0.0.1:5000/api/ad/update-status/${adId}`, {
                method: "PUT",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({negotiated_payment_amount: negotiated_payment_amount})
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await response.json();
            context.commit("updateAd", data.ad);
            console.log(data)
            context.commit("setAdStatus", data.message);
            context.commit("setSuccess", true);
        } catch (error) {
            console.error("Error negotiating ad:", error);
            context.commit("setError", error.message);
        }
    },

    async downloadReport(context, user_id) {
        try {
            context.commit("setCeleryWaiting", true);
            const token = JSON.parse(localStorage.getItem("token"));
            const response = await fetch(`http://127.0.0.1:5000/api/report/data/${user_id}`, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'campaign_report.csv';
            document.body.appendChild(a);
            a.click();
            a.remove();
        } catch (error) {
            console.error("Error downloading report:", error);
            this.$store.commit("setError", error.message);
        } finally {
            context.commit("setCeleryWaiting", false);
        }
    },

    async search(context, form) {
        try {
            const token = JSON.parse(localStorage.getItem("token"));
            const response = await fetch(`http://127.0.0.1:5000/api/search`, {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(form)
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await response.json();
            context.commit("setSearchResults", data);
        } catch (error) {
            console.error("Error performing search:", error);
            context.commit("setError", error.message);
        }
    },


    // Influencer API Calls
    async fetchAllCampaigns(context) {
        try {
            const token = JSON.parse(localStorage.getItem("token"));
            const role = JSON.parse(localStorage.getItem("role"));

            if (role !== "influencer" && role !== "admin") {
                throw new Error("User is not an influencer");
            }

            const response = await fetch("http://127.0.0.1:5000/api/campaigns-list", {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await response.json();
            context.commit("setAllCampaigns", data);
        } catch (error) {
            console.error("Error fetching all campaigns:", error);
            context.commit("setError", error.message);
        }
    },

    async fetchInfluencerCampaigns(context, influencerUsername) {
        try {
            const token = JSON.parse(localStorage.getItem("token"));
            const role = JSON.parse(localStorage.getItem("role"));

            if (role !== "influencer") {
                throw new Error("User is not an influencer");
            }

            const response = await fetch(`http://127.0.0.1:5000/api/influencer/campaigns-list/${influencerUsername}`, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await response.json();
            context.commit("setInfluencerCampaigns", data);
        } catch (error) {
            console.error("Error fetching influencer campaigns:", error);
            context.commit("setError", error.message);
        }
    },

    async fetchInfluencerAds(context, influencerUsername) {
        try {
            const token = JSON.parse(localStorage.getItem("token"));
            const role = JSON.parse(localStorage.getItem("role"));

            if (role !== "influencer") {
                throw new Error("User is not an influencer");
            }

            const response = await fetch(`http://127.0.0.1:5000/api/influencer/ads-list/${influencerUsername}`, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await response.json();
            context.commit("setInfluencerAds", data);
        } catch (error) {
            console.error("Error fetching influencer ads:", error);
            context.commit("setError", error.message);
        }
    },

    // Admin API Calls

    async fetchAllSponsors(context) {
         try {
            const token = JSON.parse(localStorage.getItem("token"));
            const response = await fetch("http://127.0.0.1:5000/api/sponsors-list", {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            });
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            const data = await response.json();
            context.commit("setSponsors", data);
        } catch (error) {
            console.error("Error fetching influencers:", error);
        }
    }, //fetching sponsors list

    async flagCampaign(context, campaignId) {
        try {
            const token = JSON.parse(localStorage.getItem("token"));
            const role = JSON.parse(localStorage.getItem("role"));

            if (role !== "admin") {
                throw new Error("User is not an admin");
            }

            const response = await fetch(`http://127.0.0.1:5000/api/campaign/flag/${campaignId}`, {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await response.json();
            console.log(data)
            //context.commit("updateCampaign", data.campaign);
            context.commit("setSuccess", true);
        } catch (error) {
            console.error("Error flagging campaign:", error);
            context.commit("setError", error.message);
        }
    },

    async unflagCampaign(context, campaignId) {
        try {
            const token = JSON.parse(localStorage.getItem("token"));
            const role = JSON.parse(localStorage.getItem("role"));

            if (role !== "admin") {
                throw new Error("User is not an admin");
            }

            const response = await fetch(`http://127.0.0.1:5000/api/campaign/unflag/${campaignId}`, {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await response.json();
            console.log(data)
            //context.commit("updateCampaign", data.campaign);
            context.commit("setSuccess", true);
        } catch (error) {
            console.error("Error flagging campaign:", error);
            context.commit("setError", error.message);
        }
    },

    async verifyInfluencer(context, influencerId) {
        try {
            const token = JSON.parse(localStorage.getItem("token"));
            const role = JSON.parse(localStorage.getItem("role"));

            if (role !== "admin") {
                throw new Error("User is not an admin");
            }

            const response = await fetch(`http://127.0.0.1:5000/api/influencer/verify/${influencerId}`, {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await response.json();
            context.commit("updateInfluencer", data.influencer);
            context.commit("setSuccess", true);
        } catch (error) {
            console.error("Error verifying influencer:", error);
            context.commit("setError", error.message);
        }
    },

    async approveSponsor(context, sponsorId) {
        try {
            const token = JSON.parse(localStorage.getItem("token"));
            const role = JSON.parse(localStorage.getItem("role"));

            if (role !== "admin") {
                throw new Error("User is not an admin");
            }

            const response = await fetch(`http://127.0.0.1:5000/api/sponsor/approve/${sponsorId}`, {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await response.json();
            context.commit("setError", data.message);
            console.log(data)
            context.commit("setSuccess", true);
        } catch (error) {
            console.error("Error verifying influencer:", error);
            context.commit("setError", error.message);
        }
    },

    async fetchUserbaseData(context) {
        try {
            const token = JSON.parse(localStorage.getItem("token"));
            const role = JSON.parse(localStorage.getItem("role"));

            if (role !== "admin") {
                throw new Error("User is not an admin");
            }

            const response = await fetch("http://127.0.0.1:5000/api/admin/userbase-data", {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await response.json();
            context.commit("setUserbaseData", data);
        } catch (error) {
            console.error("Error fetching userbase data:", error);
            context.commit("setError", error.message);
        }
    },

    async fetchCampaignData(context) {
    try {
        const token = JSON.parse(localStorage.getItem("token"));
        const role = JSON.parse(localStorage.getItem("role"));

        if (role !== "admin") {
            throw new Error("User is not an admin");
        }

        const response = await fetch("http://127.0.0.1:5000/api/admin/campaign-data", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error("Network response was not ok");
        }

        const data = await response.json();
        context.commit("setCampaignData", data);
    } catch (error) {
        console.error("Error fetching campaign data:", error);
        context.commit("setError", error.message);
    }
},

    async fetchAdsData(context) {
    try {
        const token = JSON.parse(localStorage.getItem("token"));
        const role = JSON.parse(localStorage.getItem("role"));

        if (role !== "admin") {
            throw new Error("User is not an admin");
        }

        const response = await fetch("http://127.0.0.1:5000/api/admin/ads-data", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error("Network response was not ok");
        }

        const data = await response.json();
        context.commit("setAdsData", data);
    } catch (error) {
        console.error("Error fetching ads data:", error);
        context.commit("setError", error.message);
    }
}

};
