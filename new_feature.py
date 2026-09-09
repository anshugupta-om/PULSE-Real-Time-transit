# new_feature.py

import streamlit as st
import random
import time

def render_new_feature():
    # Initialize session state variables
    if 'guardian_score' not in st.session_state:
        st.session_state.guardian_score = 0
    if 'streak_days' not in st.session_state:
        st.session_state.streak_days = 5
    if 'unlocked_rewards' not in st.session_state:
        st.session_state.unlocked_rewards = []
    if 'spin_active' not in st.session_state:
        st.session_state.spin_active = False

    st.markdown("---")
    
    # --- HEADER & STATS ---
    st.markdown("### 🎮 PULSE Guardian Arena: Live Safety Quest")
    
    score = st.session_state.guardian_score
    
    # Rank & Tier Determination
    if score >= 900:
        level, next_tier_goal, tier_badge = "Legendary Guardian", 1000, "👑 Legendary Guardian"
    elif score >= 800:
        level, next_tier_goal, tier_badge = "Elite Guardian", 900, "🌟 Elite Guardian"
    elif score >= 700:
        level, next_tier_goal, tier_badge = "Pro Commuter", 800, "👍 Pro Commuter"
    else:
        level, next_tier_goal, tier_badge = "Rookie Commuter", 700, "🚶 Rookie Commuter"

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("✨ Guardian XP", f"{score} pts", delta=f"Rank: {level}")
    with c2:
        st.metric("🔥 Safety Streak", f"{st.session_state.streak_days} Days", delta="Active Multiplier 1.2x")
    with c3:
        st.metric("🏆 Current Tier Badge", tier_badge)

    progress_val = min(score / float(next_tier_goal), 1.0)
    st.progress(progress_val, text=f"Level Progress: {score} / {next_tier_goal} XP to Next Tier")
    
    # Check for Elite Multiplier status
    has_elite = any("Elite" in perk for perk in st.session_state.unlocked_rewards)
    xp_mult = 2 if has_elite else 1
    
    # --- REWARD WALLET (GROUPED TO PREVENT DUPLICATE CARDS) ---
    st.markdown("#### 🎒 Your Reward Wallet")
    
    if st.session_state.unlocked_rewards:
        # Count frequencies so identical items stack cleanly into one card
        reward_counts = {}
        for r in st.session_state.unlocked_rewards:
            reward_counts[r] = reward_counts.get(r, 0) + 1
            
        for perk_name, count in reward_counts.items():
            col_item, col_action = st.columns([3, 1])
            multiplier_tag = f" (x{count})" if count > 1 else ""
            
            with col_item:
                if "VIP" in perk_name:
                    st.success(f"🔮 **VIP AI Concierge Pass{multiplier_tag}** — Exclusive seat availability & boarding priority active!")
                elif "Express" in perk_name:
                    st.success(f"🚀 **Express Alert{multiplier_tag}** — Rush hour platform notifications bypassed!")
                elif "Elite" in perk_name:
                    st.success(f"⭐ **Elite Status{multiplier_tag}** — All XP earnings doubled (2x BOOST active!)")
                elif "Shield" in perk_name:
                    st.success(f"🛡️ **Penalty Shield Token{multiplier_tag}** — Ready to block upcoming penalties!")
                elif "Mega Mystery Box" in perk_name:
                    st.success(f"💎 **Mega Mystery Box{multiplier_tag}** — Unopened bonus box!")
                else:
                    st.success(f"🎁 **{perk_name}{multiplier_tag}**")
                    
            with col_action:
                if "Mega Mystery Box" in perk_name:
                    if st.button("Open Box", key=f"open_box_{perk_name}", use_container_width=True):
                        st.session_state.unlocked_rewards.remove(perk_name)
                        earned = 100 * xp_mult
                        st.session_state.guardian_score += earned
                        st.balloons()
                        st.success(f"+{earned} XP!")
                        st.rerun()
                        
        # --- EXCLUSIVE VIP PASS SECTION (COMPLETELY DISTINCT FROM COACHES) ---
        has_vip = any("VIP" in p for p in st.session_state.unlocked_rewards)
        if has_vip:
            st.markdown("---")
            st.markdown("### 💺 VIP Feature: Real-Time Seat Availability & Boarding Matrix")
            st.info("💡 **Exclusive Perk Active:** Your VIP AI Concierge has analyzed current incoming train crowds and mapped out guaranteed seating zones.")
            
            vip_c1, vip_c2, vip_c3 = st.columns(3)
            with vip_c1:
                st.metric("🟢 Best Coach for Seating", "Coach C4 (Ladies/General)", delta="High Seating Probability")
            with vip_c2:
                st.metric("💺 Estimated Available Seats", "~18 Seats", delta="Low Crowd Density")
            with vip_c3:
                st.metric("🚪 Recommended Platform Gate", "Gate 2 (Fast Boarding)", delta="Zero Queue")
                
            st.markdown(
                """
                <div style="padding: 15px; background-color: #1e2530; border-radius: 8px; border-left: 5px solid #00cc66;">
                    <strong>AI Recommendation:</strong> Move towards the middle foot-over-bridge (FOB). Train #9042 arriving in 4 mins has optimum seating space in compartments C4 and C9.
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown("---")
            
    else:
        st.info("🔒 Your wallet is empty. Spin the Mystery Wheel below to win perks!")

    # --- SAFETY QUESTS & ACTIONS ---
    st.markdown("#### 🕹️ Play & Complete Safety Quests")
    
    boost_label = " (2x Active!)" if has_elite else ""
    
    col_q1, col_q2 = st.columns(2)
    with col_q1:
        if st.button(f"📢 Report Platform Hazard (+{25 * xp_mult} XP){boost_label}", use_container_width=True):
            st.session_state.guardian_score += (25 * xp_mult)
            st.balloons()
            st.success(f"Added +{25 * xp_mult} XP!")
            st.rerun()
            
        if st.button(f"🤝 Assist Passenger (+{40 * xp_mult} XP){boost_label}", use_container_width=True):
            st.session_state.guardian_score += (40 * xp_mult)
            st.success(f"Added +{40 * xp_mult} XP!")
            st.rerun()

    with col_q2:
        if st.button(f"🚶 Calm Boarding (+{15 * xp_mult} XP){boost_label}", use_container_width=True):
            st.session_state.guardian_score += (15 * xp_mult)
            st.success(f"Added +{15 * xp_mult} XP!")
            st.rerun()
            
        if st.button("🎡 Spin Safety Mystery Wheel", use_container_width=True):
            st.session_state.spin_active = True

    # Test penalty button (consumes exactly one shield token if available)
    if st.button("⚠️ Test Hazard Penalty (-30 XP)", use_container_width=True):
        shield_to_remove = None
        for item in st.session_state.unlocked_rewards:
            if "Shield" in item:
                shield_to_remove = item
                break
                
        if shield_to_remove:
            st.session_state.unlocked_rewards.remove(shield_to_remove)
            bonus = 5 * xp_mult
            st.session_state.guardian_score += bonus
            st.success(f"🛡️ Shield blocked penalty successfully! Bonus +{bonus} XP added.")
        else:
            st.session_state.guardian_score = max(0, st.session_state.guardian_score - 30)
            st.warning("⚠️ Penalty Applied (-30 XP): No Shield Token found in wallet!")
        st.rerun()

    # --- SPINNER LOGIC ---
    if st.session_state.spin_active:
        st.markdown("---")
        st.info("🎡 Spinning the Mystery Wheel...")
        
        slot = st.empty()
        pool = [
            ("✨ +50 Bonus XP", 50, "XP"),
            ("🔮 VIP AI Platform Concierge Pass", 40, "Perk"),
            ("🚀 Express Digital Boarding Alert", 30, "Perk"),
            ("💎 Mega Mystery Box", 0, "Box"),
            ("🛡️ Penalty Shield Token (1x Immunity)", 35, "Perk"),
            ("⭐ Elite Status Boost", 45, "Perk")
        ]
        
        for _ in range(5):
            rand_item, _, _ = random.choice(pool)
            slot.markdown(f"**🌀 Spinning... [{rand_item}]**")
            time.sleep(0.12)
            
        won_item, xp_val, r_type = random.choice(pool)
        slot.empty()
        
        st.balloons()
        st.success(f"🎉 **You won: {won_item}!**")
        
        if xp_val > 0:
            st.session_state.guardian_score += (xp_val * xp_mult)
            
        if r_type == "Perk":
            st.session_state.unlocked_rewards.append(won_item)
        elif r_type == "Box":
            st.session_state.unlocked_rewards.append("💎 Mega Mystery Box")
            
        if st.button("Claim Reward & Close", type="primary"):
            st.session_state.spin_active = False
            st.rerun()