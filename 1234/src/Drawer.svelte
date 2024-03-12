<script lang="ts">
  import { Button } from "$lib/components/ui/button/index.js";
  import * as Drawer from "$lib/components/ui/drawer/index.js";
  import * as Resizable from "$lib/components/ui/resizable";
</script>

<Drawer.Root>
  <Drawer.Trigger asChild let:builder>
    <Button builders={[builder]} variant="outline">Open Drawer</Button>
  </Drawer.Trigger>
  <Drawer.Content>
    <div class="mx-auto w-full max-w-8xl">
      <Drawer.Header>
        <Drawer.Title>Docs</Drawer.Title>
        <Drawer.Description>More Docs.</Drawer.Description>
      </Drawer.Header>
      <Resizable.PaneGroup
        direction="horizontal"
        class="min-h-[600px] max-h-[600px] max-w-8xl rounded-lg border"
      >
      <Resizable.Pane defaultSize={50}>
        <div class="relative h-full overflow-hidden">
          <div class="absolute inset-0 overflow-auto">
            <img src="image.png" alt="Source" class="w-full h-auto" />
          </div>
        </div>
      </Resizable.Pane>
        <Resizable.Handle withHandle />
        <Resizable.Pane defaultSize={50}>
          <div class="relative h-full overflow-hidden">
            <div class="absolute inset-0 overflow-auto">
              <iframe
                src="https://docs.google.com/document/d/e/2PACX-1vS_56PrCnlvJ_DV_MZMZ9vkGubaKtPx0lUeiGN6_ctRUNMkUEXCCXByO4OmGlJ02F1TEPDG2e6taIa_/pub?embedded=true"
                class="w-full h-full" title="Docs"
              ></iframe>
            </div>
          </div>
        </Resizable.Pane>
      </Resizable.PaneGroup>
      <Drawer.Footer>
        <Drawer.Close asChild let:builder>
          <Button builders={[builder]} variant="outline">Cancel</Button>
        </Drawer.Close>
      </Drawer.Footer>
    </div>
  </Drawer.Content>
</Drawer.Root>
