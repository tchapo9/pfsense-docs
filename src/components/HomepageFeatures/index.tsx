import type { ReactNode } from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Installation et prise en main',
    Svg: require('@site/static/img/pfSense_installation.svg').default,
    description: (
      <>
        Découvrez comment installer <strong>pfSense</strong> sur une machine
        physique ou virtuelle, effectuer la configuration initiale et prendre
        en main l'interface WebGUI étape par étape.
      </>
    ),
  },
  {
    title: 'Sécurité et administration réseau',
    Svg: require('@site/static/img/pfsense_performance.svg').default,
    description: (
      <>
        Apprenez à sécuriser votre infrastructure grâce aux
        <strong> règles de pare-feu</strong>, au
        <strong> NAT</strong>, aux <strong>VLAN</strong>, à la
        <strong> DMZ</strong>, au <strong>DHCP</strong>, au
        <strong> DNS</strong> et aux bonnes pratiques d'administration.
      </>
    ),
  },
  {
    title: 'VPN et accès distant sécurisé',
    Svg: require('@site/static/img/openvpn_pfsense.svg').default,
    description: (
      <>
        Configurez <strong>OpenVPN</strong>, <strong>IPsec</strong> ou
        <strong> WireGuard</strong> afin de permettre un accès distant sécurisé
        à votre réseau et protégez vos communications.
      </>
    ),
  },
];

function Feature({ title, Svg, description }: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>

      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((feature, index) => (
            <Feature key={index} {...feature} />
          ))}
        </div>
      </div>
    </section>
  );
}