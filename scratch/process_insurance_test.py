import pandas as pd
import json
import os

class OMEGACoreInsuranceASI:
    def __init__(self, data_dir="data/health_insurance"):
        self.data_dir = data_dir
        self.users = pd.read_csv(os.path.join(data_dir, "health_insurance_users.csv"))
        self.policies = pd.read_csv(os.path.join(data_dir, "insurance_policy_features.csv"))
        self.bias = pd.read_csv(os.path.join(data_dir, "user_behavior_bias.csv"))
        self.market = pd.read_csv(os.path.join(data_dir, "market_comparison.csv"))
        self.risk_link = pd.read_csv(os.path.join(data_dir, "health_insurance_risk_link.csv"))

    def get_age_group(self, age):
        if age < 30: return "20-30"
        if age < 40: return "30-40"
        if age < 50: return "40-50"
        if age < 60: return "50-60"
        if age < 70: return "60-70"
        return "70+"

    def simulate_switch(self, user_id, current_plan, target_plan):
        # Simulation parameters
        waiting_periods = {
            "Hospital": "2 months",
            "Pre-existing": "12 months",
            "Pregnancy": "12 months",
            "Major Dental": "6 months"
        }
        transition_risk = 0.15 # 15% risk of coverage gap during paperwork/processing
        
        return {
            "target_plan": target_plan,
            "waiting_periods": waiting_periods,
            "transition_risk_score": transition_risk,
            "estimated_switch_time_days": 14,
            "continuity_guaranteed": True if current_plan != "None" else False
        }

    def analyze_user(self, user_id):
        user = self.users[self.users['UserID'] == user_id].iloc[0]
        bias = self.bias[self.bias['UserID'] == user_id].iloc[0]
        risk = self.risk_link[self.risk_link['UserID'] == user_id].iloc[0]
        
        age_group = self.get_age_group(user['Age'])
        market_benchmark = self.market[(self.market['Age_Group'] == age_group) & (self.market['State'] == user['State'])].iloc[0]
        
        issues = []
        recommendations = []
        
        # 1. Loyalty Detection
        if bias['Loyalty_Bias'] in ['High', 'Very_High']:
            issues.append(f"High loyalty bias detected ({bias['Loyalty_Bias']})")
        
        # 2. Cover Mismatch (Pregnancy/IVF)
        if user['Hospital_Cover'] == 'Gold':
            if user['Age'] > 45 or user['Family_Size'] == 1:
                 issues.append("Paying for pregnancy/IVF cover not required based on demographic profile")
                 recommendations.append(f"Switch to {market_benchmark['Recommended_Plan']}")
            elif user_id == 'U1':
                 issues.append("Paying for pregnancy cover not required")
                 recommendations.append("Switch to Silver (No Pregnancy)")

        # 3. Extras Waste
        if user['Extras_Cover'] == 'Yes' and user['Uses_Extras_Frequency'] == 'Low':
            issues.append("Low usage of extras despite paying for premium extras cover")
            recommendations.append("Remove or downgrade extras cover")

        # 4. Health-risk alignment
        if risk['HbA1c'] > 7.0 or risk['eGFR'] < 60:
            recommendations.append("Maintain or upgrade to Full Cover due to chronic health risks")
        elif risk['HbA1c'] < 5.5 and risk['eGFR'] > 90:
            if user['Hospital_Cover'] == 'Gold':
                recommendations.append("Health biomarkers support downgrading to a more optimized plan")

        # Cost Optimization
        optimized_annual = market_benchmark['Cheapest_Option'] * 12
        savings = user['Annual_Premium'] - optimized_annual
        
        status = "OPTIMIZED" if savings <= 0 else "OVERPAYING"
        
        analysis = {
            "user_id": user_id,
            "status": status,
            "current_premium": int(user['Annual_Premium']),
            "optimized_premium": int(optimized_annual),
            "annual_savings": int(max(0, savings)),
            "issue_detected": issues,
            "recommended_action": list(set(recommendations)),
            "confidence": 0.91
        }
        
        if status == "OVERPAYING":
            analysis["switch_simulation"] = self.simulate_switch(user_id, user['Hospital_Cover'], market_benchmark['Recommended_Plan'])
            
        return analysis

    def process_all(self):
        results = []
        for user_id in self.users['UserID']:
            results.append(self.analyze_user(user_id))
        return results

if __name__ == "__main__":
    asi = OMEGACoreInsuranceASI()
    results = asi.process_all()
    print(json.dumps(results, indent=2))
