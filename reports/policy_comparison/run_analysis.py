"""
Comprehensive Policy Comparison Analysis
Hawaii Agricultural Dedication Programs - All Counties
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, '/home/user/AG-Dedicated/src')

from ag_dedicated import config
from ag_dedicated.analysis.statute_comparison import StatuteComparison

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (14, 8)

# Output directory
output_dir = Path('/home/user/AG-Dedicated/reports/policy_comparison')
output_dir.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("HAWAII AGRICULTURAL DEDICATION POLICY ANALYSIS")
print("Comprehensive Comparison Across All Counties")
print("=" * 80)
print()

# Load generated CSV data
county_summary = pd.read_csv(output_dir / 'county_summary.csv')
dedication_periods = pd.read_csv(output_dir / 'dedication_periods.csv')
requirements = pd.read_csv(output_dir / 'requirements.csv')

# ============================================================================
# 1. DEDICATION PERIOD COMPARISON
# ============================================================================
print("\n" + "=" * 80)
print("1. DEDICATION PERIOD OPTIONS")
print("=" * 80)

# Create visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Heatmap of dedication periods
periods_matrix = dedication_periods.set_index('County')
periods_matrix = periods_matrix.replace({True: 1, False: 0})

sns.heatmap(periods_matrix, annot=True, cmap='YlGn', cbar_kws={'label': 'Available'},
            fmt='d', ax=ax1, linewidths=1, linecolor='gray')
ax1.set_title('Dedication Period Availability by County', fontsize=14, fontweight='bold')
ax1.set_xlabel('')
ax1.set_ylabel('County', fontsize=12)

# Count of options per county
period_counts = periods_matrix.sum(axis=1)
period_counts.plot(kind='barh', color='steelblue', ax=ax2)
ax2.set_title('Number of Dedication Period Options', fontsize=14, fontweight='bold')
ax2.set_xlabel('Number of Options', fontsize=12)
ax2.set_ylabel('County', fontsize=12)
ax2.grid(axis='x', alpha=0.3)

# Add value labels
for i, v in enumerate(period_counts):
    ax2.text(v + 0.1, i, str(int(v)), va='center', fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / 'dedication_periods_analysis.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: dedication_periods_analysis.png")
print()

# Summary statistics
print("Dedication Period Summary:")
print(f"  • Most flexible: {period_counts.idxmax()} ({int(period_counts.max())} options)")
print(f"  • Least flexible: {period_counts.idxmin()} ({int(period_counts.min())} option)")
print(f"  • Average options per county: {period_counts.mean():.1f}")
print()

# Detailed breakdown
print("Available Periods by County:")
for idx, row in dedication_periods.iterrows():
    county = row['County']
    available = [col.replace('_year', '') for col in dedication_periods.columns[1:] if row[col]]
    print(f"  • {county}: {', '.join(available)} year options")
print()

# ============================================================================
# 2. ASSESSMENT METHOD COMPARISON
# ============================================================================
print("=" * 80)
print("2. ASSESSMENT METHODS & TAX RATES")
print("=" * 80)
print()

# Create comparison table
assessment_data = []

print("Assessment Approaches:")
print()

# Honolulu
print("HONOLULU (Percentage of Fair Market Value):")
print("  • 5-year dedication: 3% of FMV")
print("  • 10-year dedication: 1% of FMV")
print("  • Benefit: Longer commitment = 67% lower assessment")
assessment_data.append({
    'County': 'Honolulu',
    'Method': 'FMV Percentage',
    '5-year Rate': '3%',
    '10-year Rate': '1%',
    'Max Savings': '67%'
})
print()

# Hawaii
print("HAWAII (Fixed Valuation + Multiple Programs):")
print("  • Short-term (3yr): Base valuation ($3,000/acre for orchards)")
print("  • Long-term (10yr): 50% of short-term valuation")
print("  • Community Food: 30% of market value")
print("  • Requires: $2,000 min annual income")
assessment_data.append({
    'County': 'Hawaii',
    'Method': 'Fixed Valuation',
    '5-year Rate': 'N/A',
    '10-year Rate': '50% of base',
    'Max Savings': '50%'
})
print()

# Maui
print("MAUI (Tax Rate on Assessed Value):")
print("  • Tax rate: $5.74 per $1,000 assessed value")
print("  • Periods: 5, 10, 15, 20 years")
print("  • Benefit: Greater discounts for longer dedications")
assessment_data.append({
    'County': 'Maui',
    'Method': 'Tiered Discount',
    '5-year Rate': 'Base',
    '10-year Rate': 'Higher discount',
    'Max Savings': 'Progressive'
})
print()

# Kauai
print("KAUAI (Reduced Tax Rate):")
print("  • 5-year commitment only")
print("  • Reduced property tax rate (specific rate not disclosed)")
print("  • Recent policy changes (Ord. 1132)")
assessment_data.append({
    'County': 'Kauai',
    'Method': 'Reduced Rate',
    '5-year Rate': 'Reduced',
    '10-year Rate': 'N/A',
    'Max Savings': 'Undisclosed'
})
print()

# ============================================================================
# 3. REQUIREMENTS COMPARISON
# ============================================================================
print("=" * 80)
print("3. ELIGIBILITY REQUIREMENTS")
print("=" * 80)
print()

fig, ax = plt.subplots(figsize=(14, 6))

# Prepare requirements data
req_comparison = {
    'Honolulu': {
        'Land Use Minimum': '75%',
        'Income Requirement': 'Revenue-gen',
        'Application Deadline': 'No deadline',
        'Recent Changes': 'Stable'
    },
    'Hawaii': {
        'Land Use Minimum': 'Not specified',
        'Income Requirement': '$2,000/year',
        'Application Deadline': 'No deadline',
        'Recent Changes': '2023 reforms'
    },
    'Maui': {
        'Land Use Minimum': 'Not specified',
        'Income Requirement': 'Not specified',
        'Application Deadline': 'Sept 1',
        'Recent Changes': 'Ongoing review'
    },
    'Kauai': {
        'Land Use Minimum': 'Commercial farming',
        'Income Requirement': 'Not specified',
        'Application Deadline': 'July 1',
        'Recent Changes': 'Ord. 1132 (new)'
    }
}

# Create table
req_df = pd.DataFrame(req_comparison).T
req_df.index.name = 'County'

# Plot as table
ax.axis('tight')
ax.axis('off')
table = ax.table(cellText=req_df.values,
                rowLabels=req_df.index,
                colLabels=req_df.columns,
                cellLoc='left',
                loc='center',
                colWidths=[0.15, 0.15, 0.2, 0.15])

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)

# Style header
for i in range(len(req_df.columns)):
    table[(0, i)].set_facecolor('#4472C4')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Style rows
colors = ['#E7E6E6', '#FFFFFF']
for i in range(1, len(req_df) + 1):
    for j in range(-1, len(req_df.columns)):
        table[(i, j)].set_facecolor(colors[i % 2])

plt.title('Eligibility Requirements Comparison', fontsize=16, fontweight='bold', pad=20)
plt.savefig(output_dir / 'requirements_comparison.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: requirements_comparison.png")
print()

print("Key Requirement Differences:")
print()
print("APPLICATION DEADLINES:")
print("  • Honolulu & Hawaii: No specific deadline (rolling applications)")
print("  • Maui: September 1 annually")
print("  • Kauai: July 1 annually")
print()

print("MINIMUM REQUIREMENTS:")
print("  • Honolulu: 75% of usable land + revenue generation")
print("  • Hawaii: $2,000 annual gross income + proof of production")
print("  • Maui: Not specified in available documentation")
print("  • Kauai: Commercial farming commitment")
print()

print("RECENT POLICY CHANGES:")
print("  • Honolulu: Stable program (no recent major changes)")
print("  • Hawaii: 2023 reforms to prevent 'gentleman farmer' abuse")
print("  • Maui: Under review for consistency and uniformity")
print("  • Kauai: Ordinance No. 1132 - new petition requirements")
print()

# ============================================================================
# 4. POLICY FLEXIBILITY ANALYSIS
# ============================================================================
print("=" * 80)
print("4. POLICY FLEXIBILITY SCORING")
print("=" * 80)
print()

# Calculate flexibility scores
flexibility_scores = {
    'Honolulu': {
        'Period Options': 2,
        'Assessment Methods': 1,
        'Deadline Flexibility': 2,  # No deadline
        'Requirements Clarity': 2,  # Clear requirements
        'Total': 0
    },
    'Hawaii': {
        'Period Options': 2,
        'Assessment Methods': 3,  # Multiple programs
        'Deadline Flexibility': 2,  # No deadline
        'Requirements Clarity': 2,  # Clear income requirement
        'Total': 0
    },
    'Maui': {
        'Period Options': 4,  # Most options
        'Assessment Methods': 1,
        'Deadline Flexibility': 0,  # Fixed deadline
        'Requirements Clarity': 0,  # Less clear
        'Total': 0
    },
    'Kauai': {
        'Period Options': 1,  # Least options
        'Assessment Methods': 1,
        'Deadline Flexibility': 0,  # Fixed deadline
        'Requirements Clarity': 1,  # Recent changes
        'Total': 0
    }
}

# Calculate totals
for county in flexibility_scores:
    flexibility_scores[county]['Total'] = sum(
        v for k, v in flexibility_scores[county].items() if k != 'Total'
    )

# Create visualization
flex_df = pd.DataFrame(flexibility_scores).T
flex_df = flex_df.drop('Total', axis=1)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Stacked bar chart
flex_df.plot(kind='barh', stacked=True, ax=ax1,
             color=['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000'])
ax1.set_title('Policy Flexibility Components', fontsize=14, fontweight='bold')
ax1.set_xlabel('Flexibility Score', fontsize=12)
ax1.set_ylabel('County', fontsize=12)
ax1.legend(title='Components', bbox_to_anchor=(1.05, 1), loc='upper left')
ax1.grid(axis='x', alpha=0.3)

# Total scores
total_scores = pd.Series({k: v['Total'] for k, v in flexibility_scores.items()})
total_scores.plot(kind='barh', color='steelblue', ax=ax2)
ax2.set_title('Overall Flexibility Ranking', fontsize=14, fontweight='bold')
ax2.set_xlabel('Total Score', fontsize=12)
ax2.set_ylabel('County', fontsize=12)
ax2.grid(axis='x', alpha=0.3)

# Add value labels
for i, v in enumerate(total_scores):
    ax2.text(v + 0.2, i, str(int(v)), va='center', fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / 'flexibility_analysis.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: flexibility_analysis.png")
print()

print("Flexibility Ranking:")
for i, (county, score) in enumerate(total_scores.sort_values(ascending=False).items(), 1):
    print(f"  {i}. {county}: {int(score)} points")
print()

# ============================================================================
# 5. KEY FINDINGS & RECOMMENDATIONS
# ============================================================================
print("=" * 80)
print("5. KEY FINDINGS & RECOMMENDATIONS")
print("=" * 80)
print()

print("MAJOR DIFFERENCES:")
print()
print("1. DEDICATION PERIOD FLEXIBILITY:")
print("   • Maui offers the most options (5, 10, 15, 20 years)")
print("   • Kauai offers the least (only 5 years)")
print("   • Hawaii is unique with 3-year short-term option")
print()

print("2. ASSESSMENT METHODOLOGIES:")
print("   • Honolulu: Clearest (% of FMV)")
print("   • Hawaii: Most complex (multiple programs)")
print("   • Maui: Progressive (longer = more discount)")
print("   • Kauai: Least transparent")
print()

print("3. INCOME/PRODUCTION REQUIREMENTS:")
print("   • Hawaii: Most explicit ($2,000/year minimum)")
print("   • Honolulu: Qualitative (revenue-generating)")
print("   • Maui & Kauai: Not clearly specified")
print()

print("4. APPLICATION PROCESS:")
print("   • Honolulu & Hawaii: More flexible (no deadline)")
print("   • Maui & Kauai: Annual deadlines")
print()

print("POLICY TRENDS:")
print()
print("• TIGHTENING REQUIREMENTS: Hawaii's 2023 reforms show trend toward")
print("  preventing abuse by 'gentleman farmers' without real production")
print()
print("• MODERNIZATION: Kauai's Ordinance 1132 requires new petitions,")
print("  suggesting program updates and improved tracking")
print()
print("• INCENTIVE STRUCTURES: All counties use longer dedications for")
print("  greater tax benefits, but mechanisms differ significantly")
print()

print("RECOMMENDATIONS FOR POLICYMAKERS:")
print()
print("1. STANDARDIZATION: Consider more uniform requirements across")
print("   counties for ease of understanding and administration")
print()
print("2. TRANSPARENCY: All counties should clearly publish:")
print("   - Minimum income/production requirements")
print("   - Exact assessment calculation methods")
print("   - Compliance monitoring procedures")
print()
print("3. FLEXIBILITY: Hawaii's multiple program approach and Maui's")
print("   extended period options provide good models")
print()
print("4. ENFORCEMENT: Hawaii's income requirement provides measurable")
print("   compliance standard that could be adopted elsewhere")
print()

# ============================================================================
# 6. EXPORT SUMMARY REPORT
# ============================================================================
print("=" * 80)
print("6. GENERATING SUMMARY REPORT")
print("=" * 80)
print()

# Create comprehensive text report
report_path = output_dir / 'detailed_policy_analysis.txt'
with open(report_path, 'w') as f:
    f.write("=" * 80 + "\n")
    f.write("HAWAII AGRICULTURAL DEDICATION POLICY ANALYSIS\n")
    f.write("Detailed Comparison Across All Counties\n")
    f.write("=" * 80 + "\n\n")

    f.write("EXECUTIVE SUMMARY\n")
    f.write("-" * 80 + "\n")
    f.write("This analysis compares agricultural land dedication programs across\n")
    f.write("Hawaii's four counties (Honolulu, Hawaii, Maui, Kauai), examining:\n")
    f.write("• Dedication period options\n")
    f.write("• Assessment methodologies\n")
    f.write("• Eligibility requirements\n")
    f.write("• Application procedures\n")
    f.write("• Recent policy changes\n\n")

    f.write("DEDICATION PERIODS\n")
    f.write("-" * 80 + "\n")
    f.write(dedication_periods.to_string(index=False))
    f.write("\n\n")

    f.write("REQUIREMENTS\n")
    f.write("-" * 80 + "\n")
    f.write(requirements.to_string(index=False))
    f.write("\n\n")

    f.write("FLEXIBILITY SCORES\n")
    f.write("-" * 80 + "\n")
    for county, scores in flexibility_scores.items():
        f.write(f"\n{county}:\n")
        for metric, score in scores.items():
            f.write(f"  {metric}: {score}\n")
    f.write("\n")

    f.write("KEY FINDINGS\n")
    f.write("-" * 80 + "\n")
    f.write("1. Maui offers the most flexibility in dedication periods (4 options)\n")
    f.write("2. Hawaii has the clearest income requirement ($2,000/year)\n")
    f.write("3. Honolulu and Hawaii allow rolling applications (no deadline)\n")
    f.write("4. Recent reforms in Hawaii and Kauai show active policy evolution\n")
    f.write("\n")

print(f"✓ Saved: detailed_policy_analysis.txt")
print()

print("=" * 80)
print("ANALYSIS COMPLETE!")
print("=" * 80)
print()
print(f"All outputs saved to: {output_dir}")
print()
print("Generated files:")
print("  • dedication_periods_analysis.png")
print("  • requirements_comparison.png")
print("  • flexibility_analysis.png")
print("  • detailed_policy_analysis.txt")
print("  • comparison_report.txt")
print("  • county_summary.csv")
print("  • dedication_periods.csv")
print("  • requirements.csv")
print()
