Cleanup notes

Removed local `node_modules` directory under `tools/playwright-mcp-server` to reduce repository size.

Reason: node_modules should not be committed. The `.gitignore` file already contains entries to prevent these directories from being tracked in the future.

Files affected
- Deleted (local): `tools/playwright-mcp-server/node_modules/` (removed from working tree; never committed)
- Updated: `.gitignore` (already contains node_modules entries)

If you want the node_modules folder preserved on the remote for CI, consider publishing a package or using a release artifact instead.

Date: 2025-09-15
