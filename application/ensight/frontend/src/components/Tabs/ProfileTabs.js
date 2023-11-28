import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ProfileFocus from "./ProfileTabsContent/ProfileFocus";
import DiaryFocus from "./ProfileTabsContent/DiaryFocus";
import WatchlistFocus from "./ProfileTabsContent/WatchlistFocus";
import ListsFocus from "./ProfileTabsContent/ListsFocus";
import InsightFocus from "./ProfileTabsContent/InsightFocus";
import TabNavItem from "./TabNav/TabNavItem";
import TabContent from "./TabNav/TabContent";
import '../../assets/styles/components/ProfileTabs.css';

function ProfileTabs({ currentTab ,currentUserProfile}) {
    const [activeTab, setActiveTab] = useState(currentTab);
    const navigate = useNavigate();

    useEffect(() => {
        setActiveTab(currentTab);
    }, [currentTab]);

    const handleTabClick = (newTab) => {
        setActiveTab(newTab);
        // Update the URL when a new tab is clicked
        navigate(`/Profile/${newTab}`);
    };

    return (
        <div className="Tabs">
            <ul className="nav">
                <TabNavItem title="Profile" id="profile" activeTab={activeTab} setActiveTab={setActiveTab} onClick={() => handleTabClick("profile")} />
                <TabNavItem title="Diary" id="diary" activeTab={activeTab} setActiveTab={setActiveTab} onClick={() => handleTabClick("diary")} />
                <TabNavItem title="Watchlist" id="watchlist" activeTab={activeTab} setActiveTab={setActiveTab} onClick={() => handleTabClick("watchlist")} />
                <TabNavItem title="Lists" id="lists" activeTab={activeTab} setActiveTab={setActiveTab} onClick={() => handleTabClick("lists")} />
                <TabNavItem title="Insight" id="insight" activeTab={activeTab} setActiveTab={setActiveTab} onClick={() => handleTabClick("insight")} />
            </ul>
            <div className="outlet">
                <TabContent id="profile" activeTab={activeTab}>
                    <ProfileFocus currentUserProfile = {currentUserProfile}/>
                </TabContent>
                <TabContent id="diary" activeTab={activeTab}>
                    <DiaryFocus />
                </TabContent>
                <TabContent id="watchlist" activeTab={activeTab}>
                    <WatchlistFocus />
                </TabContent>
                <TabContent id="lists" activeTab={activeTab}>
                    <ListsFocus />
                </TabContent>
                <TabContent id="insight" activeTab={activeTab}>
                    <InsightFocus />
                </TabContent>
            </div>
        </div>
    );
}

export default ProfileTabs;
