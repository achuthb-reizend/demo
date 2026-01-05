#!/bin/bash

# --- CONFIGURATION ---
OWNER="<OWNER NAME>"
REPO="<REPO NAME>"

# --- 1. CODEQL EXPORT ---
echo " Exporting CodeQL Alerts..."
FILE_CODEQL="code_scanning_alerts.csv"
echo "number,created_at,severity,tags,description,file_path,start_line,end_line,ref,analysis_key_path,help,help_uri" > "$FILE_CODEQL"

gh api --paginate "repos/$OWNER/$REPO/code-scanning/alerts?state=open" | \
jq -r '.[] | [
  .number,
  .created_at,
  .rule.security_severity_level,
  (.rule.tags | join("; ")),
  .rule.description,
  .most_recent_instance.location.path,
  .most_recent_instance.location.start_line,
  .most_recent_instance.location.end_line,
  .most_recent_instance.ref,
  .analysis_key.path,
  .rule.help,
  .rule.help_uri
] | @csv' >> "$FILE_CODEQL"


# --- 2. DEPENDABOT EXPORT ---
echo " Exporting Dependabot Alerts..."
FILE_DEPENDABOT="dependabot_alerts.csv"
echo "number,created_at,cve_id,ghsa_id,summary,references,package_name,ecosystem,manifest_path,scope,relationship,vulnerable_version_range,fixed_version,fix_available" > "$FILE_DEPENDABOT"

gh api --paginate "repos/$OWNER/$REPO/dependabot/alerts?state=open" | \
jq -r '.[] | [
  .number,
  .created_at,
  .security_advisory.cve_id,
  .security_advisory.ghsa_id,
  .security_advisory.summary,
  (.security_advisory.references | map(.url) | join(" | ")),
  .dependency.package.name,
  .dependency.package.ecosystem,
  .dependency.manifest_path,
  .dependency.scope,
  .dependency.relationship,
  .security_vulnerability.vulnerable_version_range,
  .security_vulnerability.first_patched_version.identifier,
  .fix_available
] | @csv' >> "$FILE_DEPENDABOT"


# --- 3. SECRET SCANNING EXPORT ---
echo " Exporting Secret Scanning Alerts..."
FILE_SECRETS="secret_scanning_alerts.csv"
echo "number,created_at,secret_type,secret_type_display_name,service,locations,commit_sha" > "$FILE_SECRETS"

gh api --paginate "repos/$OWNER/$REPO/secret-scanning/alerts?state=open" | \
jq -r '.[] | [
  .number,
  .created_at,
  .secret_type,
  .secret_type_display_name,
  .service,
  ((.locations // []) | map(.path + ":" + (.start_line|tostring)) | join("; ")),
  .commit_sha
] | @csv' >> "$FILE_SECRETS"

echo "--------------------------------------------------"
echo " Done! Created 3 files:"
echo "   1. $FILE_CODEQL"
echo "   2. $FILE_DEPENDABOT"
echo "   3. $FILE_SECRETS"
