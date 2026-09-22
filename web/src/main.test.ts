import { describe, expect, it } from "vitest";

function dashboardContract(): { syntheticLabel: string; tabs: string[] } {
    return {
        syntheticLabel: "SYNTHETIC DATA",
        tabs: ["Overview", "Financial health", "Inclusion & voice", "Methods"],
    };
}

describe("dashboard foundation", () => {
    it("defines the synthetic-data boundary and core sections", () => {
        const contract = dashboardContract();

        expect(contract.syntheticLabel).toBe("SYNTHETIC DATA");
        expect(contract.tabs).toHaveLength(4);
        expect(contract.tabs).toContain("Methods");
    });
});
