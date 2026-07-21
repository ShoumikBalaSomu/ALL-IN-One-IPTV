# 📂 Output Folder

Generated playlists from the aggregation pipeline.

## Files

| File | Description |
|------|-------------|
| `combined_by_country.m3u` | All channels grouped by country (no verification) |
| `checked_combined_by_country.m3u` | Only verified working links, grouped by country |
| `index.html` | GitHub Pages landing page |

## Update Schedule

- **Combined playlist**: Every 6 hours
- **Verified playlist**: Every 6 hours (host-level check) + Weekly deep scan (Sunday)

## Direct URLs

```
# Combined (all channels)
https://raw.githubusercontent.com/ShoumikBalaSomu/ALL-IN-One-IPTV/main/output/combined_by_country.m3u

# Verified (working links only)
https://raw.githubusercontent.com/ShoumikBalaSomu/ALL-IN-One-IPTV/main/output/checked_combined_by_country.m3u
```

## Usage

Copy the URL above and paste it into your IPTV player as an M3U playlist source.

## Stats

Check the [GitHub Actions](https://github.com/ShoumikBalaSomu/ALL-IN-One-IPTV/actions) for the latest channel counts and verification percentages.