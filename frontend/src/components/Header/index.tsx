import LogoTransparent from "@/assets/ProjectLogo/png/TeamTact Logo - Transparent Background.png";

export function Header() {
  return (
    <header className="h-15 p-1.5 sticky top-0 bg-white z-10 border-b">
      <img src={LogoTransparent} alt="TeamTact Logo" className="h-12 w-auto" />
    </header>
  );
}
